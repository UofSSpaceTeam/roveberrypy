import threading
from Queue import Queue
import smbus
import roverMessages

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

class ExperimentThread(threading.Thread):
	def __init__(self, parent, i2cSemaphore):
		threading.Thread.__init__(self)
		self.parent = parent
		self.mailbox = Queue()
		self.i2cSem = i2cSemaphore
		self.i2c = smbus.SMBus(1)
		self.i2cAddress = 0x09
		self.drillSpeed = 0.3
		self.elevSpeed = 0.3
		self.drillDir = 0
		self.elevDir = 0
		
	def run(self):
		while True:
			drillChange = False
			data = self.mailbox.get()
			if "drillspd" in data:
				self.drillSpeed = int(data["drillspd"]) # 0 to 1
				drillChange = True
			if "elevspd" in data:
				self.drillSpeed = int(data["elevspd"]) # 0 to 1
				drillChange = True
			if "drill" in data:
				self.drillDir = int(data["drill"])
				drillChange = True
			if "elev" in data:
				self.elevDir = int(data["elev"])
				drillChange = True
			if "laser" in data:
				self.setLasers(data["laser"])
			
			if drillChange:
				self.setDrill()
	
	def setDrill(self):
		command = Command()
		command.type = CommandType.setSpeed
		command.d1 = int(self.drillSpeed * self.drillDir * 255)
		command.d2 = int(self.elevSpeed * self.elevDir * 255)
		self.sendCommand(command)
	
	def setLasers(self, laser):
		for i in range(1, 4):
			command = Command()
			print "laser " + str(i) + str(i == laser)
			command.type = CommandType.setLaser
			command.d1 = i
			command.d2 = (i == laser)
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
			print("Experiment thread got IOError")
		self.i2cSem.release()

