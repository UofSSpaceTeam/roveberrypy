from roverprocess import RoverProcess

import time
import os # used for disabling the SMBus if not running on the rover

class DriveProcess(RoverProcess):
	class CommandType:
		setMotors = 0x00
		# todo: add the other commands and functionality
	
	class Command:
		def __init__(self):
			self.header = 0xF7
			self.type = 0x00
			self.d1 = 0x0000
			self.d2 = 0x0000
			self.csum = 0x00
			self.trailer = 0xF8

	def setup(self, args):
		self.i2c = smbus.SMBus(1)
		self.i2cAddress = 0x07
		self.i2cSem = args[sem]
		self.joyAxes = [0.0, 0.0]
	
	def loop(self):
		self.setMotors(self.joyAxes)
		time.sleep(0.01)
	
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "j1y1" in message:
			print "got: " + str(message["j1y1"])
			self.joyAxes[0] = float(message["j1y1"])
		if "j1y2" in message:
			print "got: " + str(message["j1y2"])
			self.joyAxes[1] = float(message["j1y1"])
			
	def setMotors(self, speeds):
		command = Command()
		command.type = CommandType.setMotors
		command.d1 = int(speeds[0] * 255) # left
		command.d2 = int(speeds[1] * 255) # right
		self.sendCommand(command)
		
	def sendCommand(self, command):
		command.csum = (command.type + command.d1 + command.d2) % 256
		with i2cSem:
			self.i2cSem.acquire()
			self.i2c.write_byte(self.i2cAddress, command.header)
			self.i2c.write_byte(self.i2cAddress, command.type)
			self.i2c.write_byte(self.i2cAddress, command.d1 & 0xFF)
			self.i2c.write_byte(self.i2cAddress, command.d1 >> 8)
			self.i2c.write_byte(self.i2cAddress, command.d2 & 0xFF)
			self.i2c.write_byte(self.i2cAddress, command.d2 >> 8)
			self.i2c.write_byte(self.i2cAddress, command.csum)
			self.i2c.write_byte(self.i2cAddress, command.trailer)
			
			
	
	def cleanup(self):
		RoverProcess.cleanup(self)
		# your cleanup code here. e.g. stopAllMotors()
	
	# additional functions go here

