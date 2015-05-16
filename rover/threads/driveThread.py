import threading
from Queue import Queue
import smbus
import roverMessages

# matching structures from arduino
class CommandType:
	stop = 0x00
	stallEnable = 0x01
	spinEnable = 0x02
	setSpeed = 0x03
	setMotor = 0x04

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
		self.mailbox = Queue()
		self.i2c = smbus.SMBus(1)
		self.i2cAddress = 0x07
		self.i2cSem = i2cSemaphore
		
	def run(self):
		command = Command()
		leftSpeed = None
		rightSpeed = None
		throttle = 0.3
		while True:
			data = self.mailbox.get()
			if "c1j1y" in data:
				leftSpeed = int(data["c1j1y"] * 255) # -255 to 255
			if "c1j2y" in data:
				rightSpeed = int(data["c1j2y"] * 255) # -255 to 255
			if "throttle" in data:
				throttle = float(data["throttle"]) # 0.0 to 1.0
			
			if leftSpeed is not None and rightSpeed is not None:
				command.type = CommandType.setSpeed
				command.d1 = int(leftSpeed * throttle)
				command.d2 = int(rightSpeed * throttle)
				leftSpeed = None
				rightSpeed = None
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
	
