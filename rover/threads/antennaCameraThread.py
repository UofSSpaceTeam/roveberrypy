import threading
from Queue import Queue
from ServoDriver import *

class AntennaCameraThread(threading.Thread):
	def __init__(self, parent, i2cSemaphore):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "AntennaCamera"
		self.mailbox = Queue()
		self.i2cSem = i2cSemaphore
		self.servoDriver = ServoDriver()
		self.pitch = 0
		self.yaw = 0
		self.center = (1690, 950)

	def run(self):
		while True:
			data = self.mailbox.get()
			if "cameraMovement" in data:
				change = data["cameraMovement"]
				self.pitch += int(change[1]) * 15
				self.yaw += int(change[1]) * 15
				self.pitch = min(max(self.pitch, -45), 45)
				self.yaw = min(max(self.yaw, -90), 90)
				self.turnCamera(self.pitch, self.yaw)
				
	def turnCamera(self, pitch, yaw)
		try:
			self.i2cSem.acquire()
			servoDriver.setServo(0, int(pitch + self.center[0]))
			servoDriver.setServo(1, int(yaw + self.center[1]))
		except:
			print("couldn't move antenna camera.")
		self.i2cSem.release()

