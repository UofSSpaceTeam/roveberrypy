from roverprocess import RoverProcess

import time
import smbus

class CommandType:
	setSpeed = 0x00
	setPosition = 0x01

class Command:
	def __init__(self):
		self.header = 0xF7
		self.type = 0x00
		self.d1 = 0x0000
		self.d2 = 0x0000
		self.d3 = 0x0000
		self.d4 = 0x0000
		self.d5 = 0x0000
		self.d6 = 0x0000
		self.d7 = 0x0000
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

	def loop(self):
		self.setPosition(self.position)
		time.sleep(0.01)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "armAbsolute" in message:
			print "got: " + str(message["armAbsolute"])
			self.position = message["armAbsolute"]
			self.update = True
		if "armDirect" in message:
			print "got: " + str(message["armDirect"])
			self.setSpeed(message["armDirect"])
			self.update = True
                if "armThrottle" in message:
                        print "got: " + str(message["armThrottle"])
                        self.throttle = message["armThrottle"]
                        self.update = True



	def cleanup(self):
		RoverProcess.cleanup(self)
		# your cleanup code here. e.g. stopAllMotors()

	# additional functions go here
	def setPosition(self, coords):
		command = Command()
		command.type = CommandType.setPosition
		command.d1 = int(coords[0]) # x
		command.d2 = int(coords[1]) # y
		command.d3 = int(coords[2]) # z
		command.d4 = int(coords[3]) # phi
		command.d5 = int(coords[4]*255)
		command.d6 = int(coords[5]*255)
		command.d7 = int(self.throttle * 255)
		self.sendCommand(command)

	def setSpeed(self, speeds):
		command = Command()
		command.type = CommandType.setSpeed
		command.d1 = int(speeds[0]*255) # base rotation
		command.d2 = int(speeds[1]*255) # actuator 1
		command.d3 = int(speeds[2]*255) # actuator 2
		command.d4 = int(speeds[3]*50) # actuator 3
		command.d5 = int(speeds[4]*255) # hand open
		command.d6 = int(speeds[5]*190) # hand rotate
		command.d7 = int(self.throttle * 255)
		self.sendCommand(command)

	def sendCommand(self, command):
		command.csum = ((command.type + command.d1 + command.d2 + command.d3 +
			command.d4 + command.d5 + command.d6 + command.d7) % 256)
		try:
			self.i2cSem.acquire(block=True, timeout=None)
			self.i2c.write_byte(self.i2cAddress, command.header)
			self.i2c.write_byte(self.i2cAddress, command.type)
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
			self.i2c.write_byte(self.i2cAddress, command.csum)
			self.i2c.write_byte(self.i2cAddress, command.trailer)
		except IOError:
			print("Arm thread got IOError")
		self.i2cSem.release()

