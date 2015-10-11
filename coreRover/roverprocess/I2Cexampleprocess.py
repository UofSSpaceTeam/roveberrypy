from RoverProcess import RoverProcess

import time
import mraa

class CommandType:
		SET_LED = 0x00
	
class Command:
	def __init__(self):
		self.header = 0xF7
		self.type = 0x00
		self.d1 = 0x0000
		self.d2 = 0x0000
		self.csum = 0x00
		self.trailer = 0xF8

class I2CExampleProcess(RoverProcess):

	def setup(self, args):
		self.i2c = mraa.I2c(1)
		self.i2c.address(0x07)
		self.i2cSem = args["sem"]
		self.update = False
	
	def loop(self):
		val = False
		while(True):
			self.update = True
			self.setLED(0, int(val))
			val = not val;
			#print val
			time.sleep(0.2)
	
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
			
	def sendCommand(self, command):
		command.csum = (command.type + command.d1 + command.d2) % 256

		try:
			self.i2cSem.acquire(block=True, timeout=None)
			self.i2c.writeByte(command.header)
			self.i2c.writeByte(command.type)
			self.i2c.writeByte(command.d1 & 0xFF)
			self.i2c.writeByte(command.d1 >> 8)
			self.i2c.writeByte(command.d2 & 0xFF)
			self.i2c.writeByte(command.d2 >> 8)
			self.i2c.writeByte(command.csum)
			self.i2c.writeByte(command.trailer)
		except:
			print("Example thread got an I2C error")
		self.i2cSem.release()
			
	def cleanup(self):
		RoverProcess.cleanup(self)
		
	def setLED(self, ledIndex, state):
		command = Command()
		command.type = CommandType.SET_LED
		command.d1 = int(ledIndex)
		command.d2 = int(state)
		if self.update:
			self.sendCommand(command)
			self.update = False
		
		
