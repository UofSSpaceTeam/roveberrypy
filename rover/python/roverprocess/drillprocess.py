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

	def loop(self):
                self.setDrill()
		time.sleep(0.01)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "drillspd" in message:
                        self.drillSpeed = float(message["drillspd"])
		if "elevspd" in message:
                        self.elevSpeed = float(message["elevspd"])
                if "drill" in message:
                        self.drillDir = int(data["drill"])
                if "elev" in message:
                        self.elevDir = int(data["elev"])




	def cleanup(self):
		RoverProcess.cleanup(self)
		# your cleanup code here. e.g. stopAllMotors()

	# additional functions go here
        def setDrill(self):
            command = Command()
            command.type = CommandType.setSpeed
            command.d1 = int(self.drillSpeed * self.drillDir * 255)
            command.d2 = int(self.elevSpeed * self.elevDir * 255)
            print "drive", command.d1, command.d2
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

