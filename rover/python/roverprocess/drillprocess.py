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
		self.drillSpeed = 0.3
		self.elevSpeed = 0.3
		self.drillDir = 0
		self.elevDir = 0
		self.drillCw = False
		self.drillCcw = False
		self.drillDirChange = False

	def loop(self):
		self.setDrill()
		time.sleep(0.05)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "DrillSpeed" in message:
			self.drillSpeed = float(message["DrillSpeed"])
		if "DrillFeed" in message:
			self.elevSpeed = float(message["DrillFeed"])
		if "DrillUp" in message:
			self.elevDir = int(message["DrillUp"] == "True")
		if "DrillDn" in message:
			self.elevDir = -1*int(message["DrillDn"] == "True")
		if "DrillCw" in message:
			self.drillCw = (message["DrillCw"] == "True")
		if "DrillCcw" in message:
			self.drillCcw = (message["DrillCcw"] == "True")

	# additional functions go here
	def setDrill(self):
		command = Command()
		command.type = CommandType.SetSpeed
		
		if(self.drillCw and not self.drillCcw):
			self.drillDir = -1
		elif(self.drillCcw and not self.drillCw):
			self.drillDir = 1
		else:
			self.drillDir = 0
				
		
		command.d1 = int(self.drillSpeed * self.drillDir * 255)
		command.d2 = int(self.elevSpeed * self.elevDir * 255)
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
		# your cleanup code here. e.g. stopAllMotors()
