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
		drillEnable = False
		drillSpeed = 0.3
		elevSpeed = 0.3
		lasers = [0, 0, 0]
		drillDir = 0
		elevDir = 0
		while True:
			while not self.mailbox.empty():
				data = self.mailbox.get()
				
				# Only send commands when drill is enabled
				if "drillenable" in data:
					drillEnable = data["drillenable"]
					if !drillEnable:
						command.type = CommandType.stop
						command.d1 = 0
						command.d2 = 0
						self.sendCommand(command)
					
				if "drillspd" in data:
					drillSpeed = int(data["drillspd"]) # 0 to 1
				elif "elevspd" in data:
					drillSpeed = int(data["elevspd"]) # 0 to 1
					
				if "drillin" in data:
					if data["drillin"]:
						drillDir = 1
					else:
						drillDir = 0
				elif "drillout" in data:
					if data["drillout"]:
						drillDir = -1
					else:
						drillDir = 0
					
				if "elevdn" in data:
					if data["elevdn"]:
						elevDir = 1
					else:
						elevDir = 0
				elif "elevup" in data:
					if data["elevup"]:
						elevDir = -1
					else:
						elevDir = 0
						
				if "laser1" in data:
					lasers[1] = int(data["laser1"])
				elif "laser2" in data:
					lasers[2] = int(data["laser2"])
				elif "laser3" in data:
					lasers[3] = int(data["laser3"])
				
				if drillEnable:
					command.type = CommandType.setSpeed
					command.d1 = int(drillSpeed*drillDir*255)
					command.d2 = int(elevSpeed*elevDir*255)
					self.sendCommand(command)
					
							
					for i in [0, 1, 2]:
						command.type = CommandType.setLaser
						command.d1 = i
						command.d2 = lasers[i]
						self.sendCommand(command)
						
				else:
					# when drill is not enabled, run less
					time.sleep(0.5)
			
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