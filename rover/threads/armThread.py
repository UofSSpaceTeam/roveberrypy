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
		throttle = 0.3
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
			
			# send on complete input update
			if baseSpeed is not None:
				command.type = CommandType.setSpeed
				command.d1 = int(baseSpeed * throttle)
				baseSpeed = None
				self.sendCommand(command)
			time.sleep(0.01)

	def sendCommand(self, command):
		command.csum = (command.type + command.d1) % 256
		try:
			i2c.write_byte(address, command.header)
			i2c.write_byte(address, command.type)
			i2c.write_byte(address, command.d1 & 0xFF)
			i2c.write_byte(address, command.d1 >> 8)
			i2c.write_byte(address, command.csum)
			i2c.write_byte(address, command.trailer)
		except IOError:
			print("got IOError")
	

	def stop(self):
		self._Thread__stop()
