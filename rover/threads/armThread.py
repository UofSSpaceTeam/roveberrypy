import threading
from Queue import Queue
import time
import smbus

# matching structures from arduino
class CommandType:
	setSpeeds = 0x00
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

class ArmThread(threading.Thread):
	def __init__(self, parent, i2cSemaphore):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "Arm"
		self.mailbox = Queue()
		self.i2cSem = i2cSemaphore
		self.i2c = smbus.SMBus(1)
		self.i2cAddress = 0x08
		self.throttle = 0.5
		self.period = 0.25
		self.position = None

	def run(self):
		while True:
			if self.position is not None: # absolute mode
				self.setPosition(self.position)
				time.sleep(self.period)
				if self.mailbox.empty(): # don't block in absolute mode
					continue
			data = self.mailbox.get() # only block in direct mode
			if "armAbsolute" in data:
				self.position = data["armAbsolute"]
			if "armDirect" in data:
				self.setSpeed(data["armDirect"])
				self.position = None
			if "armThrottle" in data:
				self.throttle = (data["armThrottle"])		
	
	def setPosition(self, coords):
		command = Command()
		command.type = CommandType.setPosition
		command.d1 = int(coords[0]) # x
		command.d2 = int(coords[1]) # y 
		command.d3 = int(coords[2]) # z
		command.d4 = int(coords[3]) # phi
		command.d5 = int(0)
		command.d6 = int(0)
		command.d7 = int(self.throttle * 255)
		self.sendCommand(command)
	
	def setSpeed(self, speeds):
		command = Command()
		command.type = CommandType.setSpeed
		command.d1 = int(speeds[0]) # base rotation
		command.d2 = int(speeds[1]) # actuator 1
		command.d3 = int(speeds[2]) # actuator 2
		command.d4 = int(speeds[3]) # actuator 3
		command.d5 = int(0) # hand rotation
		command.d6 = int(0) # hand open/close
		command.d7 = int(self.throttle * 255)
		self.sendCommand(command)

	def sendCommand(self, command):
		command.csum = ((command.type + command.d1 + command.d2 + command.d3 +
			command.d4 + command.d5 + command.d6 + command.d7) % 256)
		try:
			self.i2cSem.acquire()
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

