from roverprocess import RoverProcess

import time
import smbus

class Command:
	def __init__(self):
		self.header = 0xF7
		self.d1 = 0x0000
		self.d2 = 0x0000
		self.d3 = 0x0000
		self.d4 = 0x0000
		self.d5 = 0x0000
		self.d6 = 0x0000
		self.d7 = 400
		self.d8 = 400
		self.d9 = 400
		self.csum = 0x00
		self.trailer = 0xF8

class ArmProcess(RoverProcess):

	def setup(self, args):
		self.i2c = smbus.SMBus(1)
		self.i2cAddress = 0x08
		self.i2cSem = args["sem"]
		self.joyAxes = [0.0, 0.0]
		self.update = False
		self.IKupdate = False
		self.position = None
		self.throttle = 0.5
		self.command = Command()
		
		# Smart state detection
		self.lastd1 = 0
		self.lastd2 = 0
		self.lastd3 = 0
		self.xbutton = 0
		self.bbutton = 0
		self.abutton = 0
		self.ybutton = 0
		self.lastd6 = 0

	def loop(self):
		if self.update:
			print "armcommand"
			self.sendCommand(self.command)
			self.update = False
		time.sleep(0.01)
		#print "armloop"

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		
		# Inverse Kin packets diable controller
		if "IK_XVal" in message:
			self.command.d7 = int(message["IK_XVal"])
			self.update = True

		if "IK_YVal" in message:
			self.command.d8 = int(message["IK_YVal"])
			self.update = True

		if "IK_WristVal" in message:
			self.command.d9 = int(message["IK_WristVal"])
			self.update = True
		
		# Inverse Kin Gripper Controls
		if "armWristCw" in message:
			self.update = True	

		if "armWristCcw" in message:
			self.update = True

		if "armGrpClose" in message:
			self.update = True

		if "armGrpOpen" in message:
			self.update = True


		# Manual Arm Controls
			
		if "inputTwoLeftY" in message:
			msg = int(message["inputTwoLeftY"]*255)
			if(self.lastd2 == 0 and msg == self.lastd2):
				pass
			else:
				self.command.d2 = msg
				self.lastd2 = msg
				self.update = True

		if "inputTwoRightY" in message:
			msg = int(message["inputTwoRightY"]*255)
			if(self.lastd1 == 0 and msg == self.lastd1):
				pass
			else:
				self.command.d1 = msg
				self.lastd1 = msg
				self.update = True

		if "inputTwoLeftX" in message:
			msg = int(message["inputTwoLeftX"]*255)
			if(self.lastd6 == 0 and msg == self.lastd6):
				pass
			else:
				self.command.d6 = msg
				self.lastd6 = msg
				self.update = True

		if "armBaseSlider" in message:
			msg = int(message["armBaseSlider"]*255)
			if(self.lastd6 == 0 and msg == self.lastd6):
				pass
			else:
				self.command.d6 = msg
				self.lastd6 = msg
				self.update = True
			
		# Gripper Controls
			
		
		if "inputTwoBButton" in message:
			msg = 255*int(message["inputTwoBButton"]== "True")
			if(self.bbutton == 0 and msg == self.bbutton):
				pass
			else:
				self.command.d4 = msg
				self.bbutton = msg
				self.update = True
			
		if "inputTwoXButton" in message:
			msg = -255*int(message["inputTwoXButton"]== "True")
			if(self.xbutton == 0 and msg == self.xbutton):
				pass
			else:
				self.command.d4 = msg
				self.xbutton = msg
				self.update = True
		
		if "inputTwoAButton" in message:
			msg = 255*int(message["inputTwoAButton"]== "True")
			if(self.abutton == 0 and msg == self.abutton):
				pass
			else:
				self.command.d5 = msg
				self.abutton = msg
				self.update = True
			
		if "inputTwoYButton" in message:
			msg = -255*int(message["inputTwoYButton"]== "True")
			if(self.ybutton == 0 and msg == self.ybutton):
				pass
			else:
				self.command.d5 = msg
				self.ybutton = msg
				self.update = True
				
		# if self.xbutton==0 and self.bbutton==0:
			# self.command.d4 = 0
			
		# if self.abutton==0 and self.ybutton==0:
			# self.command.d5 = 0
			


	def cleanup(self):
		RoverProcess.cleanup(self)
		# your cleanup code here. e.g. stopAllMotors()

	# additional functions go here

	def sendCommand(self, command):
		command.csum = ((command.d1 + command.d2 + command.d3 +
			command.d4 + command.d5 + command.d6 + command.d7 + command.d8 + command.d9) % 256)
			
		print "arm", command.d4, command.d5, command.d6
		try:
			self.i2cSem.acquire(block=True, timeout=None)
			self.i2c.write_byte(self.i2cAddress, command.header)
			self.i2c.write_byte(self.i2cAddress, command.d1 & 0xFF)
			self.i2c.write_byte(self.i2cAddress, command.d1 >> 8)
			self.i2c.write_byte(self.i2cAddress, command.d2 & 0xFF)
			self.i2c.write_byte(self.i2cAddress, command.d2 >> 8)
			self.i2c.write_byte(self.i2cAddress, command.d3 & 0xFF)
			self.i2c.write_byte(self.i2cAddress, command.d3 >> 8)
			self.i2c.write_byte(self.i2cAddress, command.d4 & 0xFF)
			self.i2c.write_byte(self.i2cAddress, command.d4 >> 8)
			self.i2c.write_byte(self.i2cAddress, command.d5 & 0xFF)
			self.i2c.write_byte(self.i2cAddress, command.d5 >> 8)
			self.i2c.write_byte(self.i2cAddress, command.d6 & 0xFF)
			self.i2c.write_byte(self.i2cAddress, command.d6 >> 8)
			self.i2c.write_byte(self.i2cAddress, command.d7 & 0xFF)
			self.i2c.write_byte(self.i2cAddress, command.d7 >> 8)
			self.i2c.write_byte(self.i2cAddress, command.d8 & 0xFF)
			self.i2c.write_byte(self.i2cAddress, command.d8 >> 8)
			self.i2c.write_byte(self.i2cAddress, command.d9 & 0xFF)
			self.i2c.write_byte(self.i2cAddress, command.d9 >> 8)
			self.i2c.write_byte(self.i2cAddress, command.csum)
			self.i2c.write_byte(self.i2cAddress, command.trailer)
		except IOError:
			print("Arm thread got IOError")
		self.i2cSem.release()

