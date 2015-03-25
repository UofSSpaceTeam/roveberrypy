
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
address = 0x07

class driveThread(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "driveThread"
		self.exit = False
		self.mailbox = Queue()
		self.enabled = False

		
	def run(self):
		command = Command()
		leftSpeed = None
		rightSpeed = None
		throttle = 0.3
		while True:
			while not self.mailbox.empty():
				data = self.mailbox.get()
				print data
				if "dMode" in data:
					self.enabled = (data["dMode"])
				if self.enabled:
					if "c1j1y" in data:
						leftSpeed = int(data["c1j1y"] * 255) # -255 to 255
					elif "c1j2y" in data:
						rightSpeed = int(data["c1j2y"] * 255) # -255 to 255
					elif "throttle" in data:
						throttle = float(data["throttle"]) # 0.0 to 1.0
			
			# send on complete input update
			if leftSpeed is not None and rightSpeed is not None:
				command.type = CommandType.setSpeed
				command.d1 = int(leftSpeed * throttle)
				command.d2 = int(rightSpeed * throttle)
				leftSpeed = None
				rightSpeed = None
				self.sendCommand(command)
			time.sleep(0.01)
	
	
	def sendCommand(self, command):
		command.csum = (command.type + command.d1 + command.d2) % 256
		try:
			i2c.write_byte(address, command.header)
			i2c.write_byte(address, command.type)
			i2c.write_byte(address, command.d1 & 0xFF)
			i2c.write_byte(address, command.d1 >> 8)
			i2c.write_byte(address, command.d2 & 0xFF)
			i2c.write_byte(address, command.d2 >> 8)
			i2c.write_byte(address, command.csum)
			i2c.write_byte(address, command.trailer)
		except IOError:
			print("got IOError")
	
	
	def stop(self):
		self._Thread__stop()

