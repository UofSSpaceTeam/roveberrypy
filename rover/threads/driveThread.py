
import roverMessages
import threading
import json
from Queue import Queue
import time
import unicodeConvert
import smbus
import struct

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
	
	def pack(self):
		return struct.pack("BBhhBB", self.header, self.type, self.d1, self.d2,
			self.csum, self.trailer)


convert = unicodeConvert.convert

# Setting up I2C
i2c = smbus.SMBus(1)
address = 0x07

class driveThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "driveThread"
		self.exit = False
		self.mailbox = Queue()

	def run(self):
		command = Command()
		leftSpeed = None
		rightSpeed = None
		while not self.exit:
			while not self.mailbox.empty():
				data = self.mailbox.get()
				if "c1j1y" in data:
					leftSpeed = int(data.pop() * 255) # -255 to 255
				elif "c1j2y" in data:
					rightSpeed = int(data.pop() * 255) # -255 to 255

			if leftSpeed is not None and rightSpeed is not None:
				command.type = CommandType.setSpeed
				command.d1 = leftSpeed
				command.d2 = rightSpeed
				command.csum = (command.type + command.d1 + command.d2) % 256
				message = command.pack()
				for byte in message:
					i2c.write_byte(address, byte)
				leftSpeed = None
				rightSpeed = None
			time.sleep(0.01)

	def stop(self):
		self.exit = True

