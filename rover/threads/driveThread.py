
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
		while not self.exit:
			if not self.mailbox.empty():
				data = self.mailbox.get()
				if "c1t" in data:
					val = int(data.pop()*100 + 100)
					i2c.write_byte(address, 0xF0)
					i2c.write_byte(address, val)
			else:
				pass
				#print "No Data!"
			time.sleep(0.01)

	def stop(self):
		self.exit = True
