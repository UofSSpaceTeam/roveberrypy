
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
	def __init__(self, parent, i2cSemaphore):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "armThread"
		self.exit = False
		self.mailbox = Queue()
		self.i2cSem = i2cSemaphore

	def run(self):
		command = Command()
		baseSpeed = None
		x = None
		y = None
		z = None
		phi = None
		print "arm thread started"
		while True:
			while not self.mailbox.empty():
				data = self.mailbox.get()
				#print data
				if "c2j1x" in data:
					x = int(data["c2j1x"] * 10) # -255 to 255
					#print baseSpeed
				if "c2j1y" in data:
					y = int(data["c2j1y"] * 10)
					#print L1
				if "c2j2x" in data:
					z = int(data["c2j2x"] * 10)
					#print L2
				if "c2j2y" in data:
					phi = int(data["c2j2y"] * 10)
				if "arm-gui_x" in data:
					x = int(data["arm-gui_x"]) * 10)
				if "arm-gui_y" in data:
					y = int(data["arm-gui_y"]) * 10)
				if "arm-gui_z" in data:
					z = int(data["arm-gui_z"]) * 10)
				if "arm-gui_phi" in data:
					phi = int(data["arm-gui_phi"]) * 10)

			
			if x is not None and y is not None and z is not None and phi is not None:
				command.type = CommandType.setPos
				command.d1 = int(x)
				command.d2 = int(y)
				command.d3 = int(z)
				command.d4 = int(phi)
				x = None
				y = None
				z = None
				phi = None
				self.sendCommand(command)
			time.sleep(0.01)

	def sendCommand(self, command):
		command.csum = (command.type + command.d1 + command.d2 + command.d3 + command.d4) % 256
		try:
			self.i2cSem.acquire()
			#print(command.d1)
			#print(command.d2)
			#print(command.d3)
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
			self.i2cSem.release()
		except IOError:
			print("Arm thread got IOError")
			self.i2cSem.release()
	

	def stop(self):
		self._Thread__stop()
