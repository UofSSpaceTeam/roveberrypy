from roverprocess import RoverProcess

import time
import smbus

class CommandType:
	stop = 0x00
	SetSpeed = 0x01

class Command:
	def __init__(self):
		self.header = 0xF7
		self.type = 0x00
		self.d1 = 0x0000
		self.d2 = 0x0000
		self.csum = 0x00
		self.trailer = 0xF8

class DrillProcess(RoverProcess):

	def setup(self, args):
		self.i2c = smbus.SMBus(1)
		self.i2cAddress = 0x09
		self.i2cSem = args["sem"]
		self.rotation = 0.0
		self.translation = 0.0

	def loop(self):
		self.setDrill()
		time.sleep(0.2)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "drillHeartbeat" in message:
			self.setShared("drillHeartbeat", True)
		if "drillRotation" in message:
			self.rotation = float(message["drillRotation"])
		if "drillTranslation" in message:
			self.translation = float(message["drillTranslation"])

	def setDrill(self):
		command = Command()
		command.type = CommandType.SetSpeed
		command.d1 = int(self.rotation * 255)
		command.d2 = int(self.translation * 255)
		self.sendCommand(command)

	def sendCommand(self, command):
		command.csum = ((command.type + command.d1 + command.d2) % 256)
		try:
			self.i2cSem.acquire(block=True, timeout=None)
			self.i2c.write_byte(self.i2cAddress, command.header)
			self.i2c.write_byte(self.i2cAddress, command.type)
			self.i2c.write_byte(self.i2cAddress, command.d1 & 0xFF)
			self.i2c.write_byte(self.i2cAddress, command.d1 >> 8)
			self.i2c.write_byte(self.i2cAddress, command.d2 & 0xFF)
			self.i2c.write_byte(self.i2cAddress, command.d2 >> 8)
			self.i2c.write_byte(self.i2cAddress, command.csum)
			self.i2c.write_byte(self.i2cAddress, command.trailer)
		except IOError:
			print("Arm thread got IOError")
		self.i2cSem.release()

	def cleanup(self):
		RoverProcess.cleanup(self)
