import threading
import pygame
from Queue import Queue
import time

class InputThread(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.parent = parent
		self.period = 0.2
		self.mailbox = Queue()
		pygame.init()
		self.driveController = None
		self.armController = None
		if pygame.joystick.get_count() > 0:
			self.driveController = pygame.joystick.Joystick(0)
			self.driveController.init()
		if pygame.joystick.get_count() > 1:
			self.armController = pygame.joystick.Joystick(1)
			self.armController.init()
		self.armMode = "disabled" # absolute / relative / direct / disabled
		self.armCoords = [400, 0, 400, 0, 0, 0]
		self.armThrottle = 0.5
		self.driveThrottle = 0.3
		self.grpThrottle = 0.5
	
	def run(self):
		while True:
			time.sleep(self.period)
			armChanged = False
			while not self.mailbox.empty():
				data = self.mailbox.get()
				print data
				if "armRad" in data and self.armMode == "absolute":
					self.armCoords[0] = int(data["armRad"])
					armChanged = True
					print "got armrad"
				if "armBase" in data and self.armMode == "absolute":
					self.armCoords[1] = int(data["armBase"])*-1.0
					armChanged = True
				if "armZ" in data and self.armMode == "absolute":
					self.armCoords[2] = int(data["armZ"])
					armChanged = True
				if "armPhi" in data and self.armMode == "absolute":
					self.armCoords[3] = int(data["armPhi"])
					armChanged = True
				if "armGrpOpen" in data:
					a = data["armGrpOpen"]*-255*self.grpThrottle
					print a
					self.armCoords[5] = data["armGrpOpen"]*-255
				if "armGrpRot" in data:
					self.armCoords[4] = data["armGrpRot"]*255
				if "driveThrottle" in data:
					self.driveThrottle = data["driveThrottle"]
				if "armThrottle" in data:
					self.armThrottle = data["armThrottle"]
				if "grpThrottle" in data:
					self.grpThrottle = data["grpThrottle"]
				if "armMode" in data:
					kin = data["armMode"][0]
					cont = data["armMode"][1]
					if not kin and not cont:
						self.armMode = "disabled"
					elif not kin and cont:
						self.armMode = "direct"
					elif kin and not cont:
						self.armMode = "absolute"
					
			pygame.event.pump()
			if self.driveController is not None:
				self.sendDriveMessages()
				self.sendAntennaCameraMessages()
			if ((self.armMode == "absolute" and armChanged)
				or self.armController is not None):
				self.sendArmMessages()		
	
	def sendArmMessages(self):
		if self.armMode != "disabled":
			msg = {"armThrottle":self.armThrottle}
			self.parent.commThread.mailbox.put(msg)
		if self.armMode == "absolute":
			self.sendArmCoords()
		elif self.armMode == "direct":
			baseSpeed = self.filter(self.armController.get_axis(0)) * -1.0 * self.armThrottle
			ac1Speed = self.filter(self.armController.get_axis(3)) * -1.0
			ac2Speed = self.filter(self.armController.get_axis(1)) * -1.0
			wristSpeed = self.filter(self.armController.get_hat(0)[1])
			gripperRotate = (self.armController.get_hat(0)[0])
			gripperOpen = self.filter(self.armController.get_axis(2)) * -1.0 *self.grpThrottle
			msg = {"armDirect":(baseSpeed, ac1Speed, ac2Speed, wristSpeed, gripperRotate, gripperOpen)}
			self.parent.commThread.mailbox.put(msg)
	
	def sendArmCoords(self):
		msg = {"armAbsolute":self.armCoords}
		self.parent.commThread.mailbox.put(msg)
	
	def sendAntennaCameraMessages(self):
		cameraMovement = self.driveController.get_hat(0)
		msg = {"cameraMovement":cameraMovement}
		self.parent.commThread.mailbox.put(msg)
	
	def sendDriveMessages(self):
		leftSpeed = self.filter(self.driveController.get_axis(1)) * -1.0
		rightSpeed = self.filter(self.driveController.get_axis(3)) * -1.0
		leftSpeed *= self.driveThrottle
		rightSpeed *= self.driveThrottle
		msg = {"motorSpeeds":(leftSpeed, rightSpeed)}
		self.parent.commThread.mailbox.put(msg)
	
	def filter(self, value):
		if abs(value) < 0.25: # deadzone
			return 0.0
		elif value > 1.0:
			return 1.0
		elif value < -1.0:
			return -1.0
		return value
