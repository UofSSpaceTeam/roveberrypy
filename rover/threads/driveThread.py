import threading
from Queue import Queue
import smbus

# matching structures from arduino
class CommandType:
	setMotors = 0x00

class Command:
	def __init__(self):
		self.header = 0xF7
		self.type = 0x00
		self.d1 = 0x0000
		self.d2 = 0x0000
		self.csum = 0x00
		self.trailer = 0xF8

class DriveThread(threading.Thread):
	def __init__(self, parent, i2cSemaphore):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "Drive"
		self.mailbox = Queue()
		self.i2c = smbus.SMBus(1)
		self.i2cAddress = 0x07
		self.i2cSem = i2cSemaphore
		self.cameraPitch = 0
		self.cameraYaw = 0
		
	def run(self):
		while True:
			data = self.mailbox.get()
			if "motorSpeeds" in data:
				self.setMotors(data["motorSpeeds"])


	def setMotors(self, speeds):
		command = Command()
		command.type = CommandType.setMotors
		command.d1 = speeds[0] # left
		command.d2 = -speeds[1] # right
		self.sendCommand(command)
		
	def sendCommand(self, command):
		command.csum = (command.type + command.d1 + command.d2) % 256
		try:
			self.i2cSem.acquire()
			self.i2c.write_byte(self.i2cAddress, command.header)
			self.i2c.write_byte(self.i2cAddress, command.type)
			self.i2c.write_byte(self.i2cAddress, command.d1 & 0xFF)
			self.i2c.write_byte(self.i2cAddress, command.d1 >> 8)
			self.i2c.write_byte(self.i2cAddress, command.d2 & 0xFF)
			self.i2c.write_byte(self.i2cAddress, command.d2 >> 8)
			self.i2c.write_byte(self.i2cAddress, command.csum)
			self.i2c.write_byte(self.i2cAddress, command.trailer)
		except IOError:
			print("Drive thread got IOError")
		self.i2cSem.release()

