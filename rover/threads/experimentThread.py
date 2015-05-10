
import roverMessages
import threading
import json
from Queue import Queue
import time
import smbus
import struct
from unicodeConvert import convert

# matching structures from arduino
class CommandType:
	stop = 0x00
	setSpeed = 0x01
	setLaser = 0x02

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
address = 0x09

class driveThread(threading.Thread):
	def __init__(self, parent, i2cSemaphore):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "driveThread"
		self.exit = False
		self.mailbox = Queue()
		self.i2cSem = i2cSemaphore
		
	def run(self):
		command = Command()
		drillSpeed = None
		elevSpeed = None
		lasers = [0, 0, 0]
		scale = 1
		while True:
			while not self.mailbox.empty():
				data = self.mailbox.get()
				#print data
				if "c1j1y" in data:
					drillSpeed = int(data["c1j1y"] * 255) # -255 to 255
				elif "c1j2y" in data:
					elevSpeed = int(data["c1j2y"] * 255) # -255 to 255
					
				if "laser1" in data:
					lasers[1] = int(data["laser1"])
				elif "laser2" in data:
					lasers[2] = int(data["laser2"])
				elif "laser3" in data:
					lasers[3] = int(data["laser3"])
				
			# send on complete input update
			if drillSpeed is not None and elevSpeed is not None:
				command.type = CommandType.setSpeed
				command.d1 = int(drillSpeed * scale)
				command.d2 = int(elevSpeed * scale)
				leftSpeed = None
				rightSpeed = None
				self.sendCommand(command)
				
			for i in [0, 1, 2]:
				if lasers[i] is not None:
					command.type = CommandType.setLaser
					command.d1 = i
					command.d2 = lasers[i]
					lasers[i] = None
					self.sendCommand(command)
			time.sleep(0.01)
	
	
	def sendCommand(self, command):
		command.csum = (command.type + command.d1 + command.d2) % 256
		try:
			self.i2cSem.acquire()
			i2c.write_byte(address, command.header)
			i2c.write_byte(address, command.type)
			i2c.write_byte(address, command.d1 & 0xFF)
			i2c.write_byte(address, command.d1 >> 8)
			i2c.write_byte(address, command.d2 & 0xFF)
			i2c.write_byte(address, command.d2 >> 8)
			i2c.write_byte(address, command.csum)
			i2c.write_byte(address, command.trailer)
			self.i2cSem.release()
		except IOError:
			print("Experiment thread got IOError")
			self.i2cSem.release()
	
	
	def stop(self):
		self._Thread__stop()

