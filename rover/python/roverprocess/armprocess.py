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
		self.position = None
		self.throttle = 0.5
		self.command = Command()

	def loop(self):
		if self.update:
			print "armcommand"
			self.sendCommand(self.command)
			self.update = False
		time.sleep(0.01)
		#print "armloop"

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "inputTwoLeftY" in message:
			print "arm got message"
			self.command.d2 = int(message["inputTwoLeftY"]*255)
			self.update = True

		if "inputTwoRightY" in message:
			self.command.d1 = int(message["inputTwoRightY"]*255)
			self.update = True

		if "inputTwoLeftX" in message:
			self.command.d6 = int(message["inputTwoLeftX"]*255)
			self.update = True

		if "armBaseSlider" in message:
			self.command.d6 = int(message["armBaseSlider"]*255)
			self.update = True

		if "IK_XVal" in message:
			self.command.d7 = int(message["IK_XVal"]*10)
			self.update = True

		if "IK_YVal" in message:
			self.command.d8 = int(message["IK_YVal"]*10)
			self.update = True

		if "IK_WristVal" in message:
			self.command.d9 = int(message["IK_WristVal"]*10)
			self.update = True

		if "armWristCw" in message:
			self.update = True

		if "armWristCcw" in message:
			self.update = True

		if "armGrpClose" in message:
			self.update = True

		if "armGrpOpen" in message:
			self.update = True




	def cleanup(self):
		RoverProcess.cleanup(self)
		# your cleanup code here. e.g. stopAllMotors()

	# additional functions go here

	def sendCommand(self, command):
		command.csum = ((command.d1 + command.d2 + command.d3 +
			command.d4 + command.d5 + command.d6 + command.d7 + command.d8 + command.d9) % 256)
			
		print "arm", command.d1, command.d2, command.d7
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

