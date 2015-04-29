import roverMessages
import threading
import json
from Queue import Queue
import time
from unicodeConvert import convert

import smbus
import struct

# matching structures from arduino
class CommandType:
	stop = 0x00
	setPos = 0x01
	nudge = 0x02
class Command:
	def __init__(self):
		self.header = 0xF7
		self.type = 0x00
		self.d1 = 0x0000
		self.d2 = 0x0000
		self.d3 = 0x0000
		self.d4 = 0x0000
		self.csum = 0x00
		self.trailer = 0xF8

# Setting up I2C
i2c = smbus.SMBus(1)
address = 0x08

class armThread(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "armThread"
		self.exit = False
		self.mailbox = Queue()
		self.enabled = False

	def run(self):
		command = Command()
		baseSpeed = None
		L1 = None
		L2 = None
		L3 = None
		print "arm thread started"
		while True:
			while not self.mailbox.empty():
				data = self.mailbox.get()
				if "aMode" in data:
					self.enabled = (data["aMode"])
				if self.enabled:
					if "c1t" in data:
						baseSpeed = int(data["c1t"] * 255) # -255 to 255
						print baseSpeed
					if "c1j1y" in data:
						L1 = int(data["c1j1y"] * 255)
						print L1
			
			baseSpeed = 128
			L1 = 101
			L2 = 56
			L3 = 98
			# send on complete input update
			if baseSpeed is not None and L1 is not None and L2 is not None:
				command.type = CommandType.setPos
				command.d1 = int(baseSpeed)
				command.d2 = int(L1)
				command.d3 = int(L2)
				command.d4 = int(L3)
				baseSpeed = None
				L1 = None
				L2 = None
				L3 = None
				self.sendCommand(command)
			time.sleep(0.01)

	def sendCommand(self, command):
		command.csum = (command.type + command.d1 + command.d2 + command.d3 + command.d4) % 256
		try:
			i2c.write_byte(address, command.header)
			i2c.write_byte(address, command.type)
			i2c.write_byte(address, command.d1 & 0xFF)
			i2c.write_byte(address, command.d1 >> 8)
			i2c.write_byte(address, command.d2 & 0xFF)
			i2c.write_byte(address, command.d2 >> 8)
			i2c.write_byte(address, command.d3 & 0xFF)
			i2c.write_byte(address, command.d3 >> 8)
			i2c.write_byte(address, command.d4 & 0xFF)
			i2c.write_byte(address, command.d4 >> 8)
			i2c.write_byte(address, command.csum)
			i2c.write_byte(address, command.trailer)
		except IOError:
			print("got IOError")
	

	def stop(self):
		self._Thread__stop()
