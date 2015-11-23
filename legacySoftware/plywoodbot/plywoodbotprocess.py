#****************************************
#use plywoodbot.py instead
#****************************************

import os, sys
sys.dont_write_bytecode = True
import time
#uncomment when on pi 
#import smbus
import pygame
import multiprocessing

class CommandType:
		setMotors = 0x00
		#todo: add the other commands and functionality

class Command:
	def __init__(self):
		self.header = 0xF7
		self.type = 0x00
		self.d1 = 0x0000
		self.d2 = 0x0000
		self.csum = 0x00
		self.trailer = 0xF8
		
class plywoodbotProcess:

	def __init__(self, **kwargs):
		Process.__init__(self)
		self.uplink = kwargs["uplink"]
		self.downlink = kwargs["downlink"]
		self._state = dict()
		self._stateSem = BoundedSemaphore()
		self._args = kwargs
		self.load = True

	def run(self):
		receiver = RoverProcess.ReceiverThread(
			self.downlink, self._state, self._stateSem, self)
		receiver.start()
		try:
			self.setup(self._args)
			while True:
				self.loop()
		except KeyboardInterrupt:
			self.cleanup()
			sys.exit(0)
		except:
			self.cleanup()
			raise

	#==============================================================
	
	def setup(self):
	
		#uncomment when on pi
		#self.i2c = smbus.SMBus(1)
		self.i2cAddress = 0x07
		self.i2cSem = args["sem"]    
		self.joyAxes = [0.0, 0.0]
		
		self.driveController = None
		if pygame.joystick.get_count() > 0:
			self.driveController = pygame.joystick.Joystick(0)
			self.driveController.init()
		else:
			print("No controller") 
	
		
	def loop(self):
		pygame.event.pump()
		if self.driveController is not None:
			self.getContoller()
		
		self.setMotors(self.joyAxes)
		time.sleep(0.01)
		
	#==================================================================
	#controller 
	
	def getContoller(self):
		self.joyAxes[0] = self.filter(self.driveController.get_axis(1))
		self.joyAxes[1] = self.filter(self.driveController.get_axis(3))
		
	def filter(self, value):
		if abs(value) < 0.25: # deadzone
			return 0.0
		elif value > 1.0:
			return 1.0
		elif value < -1.0:
			return -1.0
		return value

	#===================================================================
	#motors
	
	def setMotors(self, speeds):
		command = Command()
		command.type = CommandType.setMotors
		command.d1 = int(speeds[0] * 255) # left
		print "left input", command.d1
		command.d2 = int(speeds[1] * 255) # right
		print "right input", command.d2
		
		self.sendCommand(command)
		
	def sendCommand(self, command):
		command.csum = (command.type + command.d1 + command.d2) % 256
		try:
			print("sending command to motors")
			#uncomment when on pi
			#self.i2cSem.acquire(block=True, timeout=None)
			#self.i2c.write_byte(self.i2cAddress, command.header)
			#self.i2c.write_byte(self.i2cAddress, command.type)
			#self.i2c.write_byte(self.i2cAddress, command.d1 & 0xFF)
			#self.i2c.write_byte(self.i2cAddress, command.d1 >> 8)
			#self.i2c.write_byte(self.i2cAddress, command.d2 & 0xFF)
			#self.i2c.write_byte(self.i2cAddress, command.d2 >> 8)
			#self.i2c.write_byte(self.i2cAddress, command.csum)
			#self.i2c.write_byte(self.i2cAddress, command.trailer)
		except IOError:
			print("Drive thread got IOError")
		self.i2cSem.release()
		
	#=============================================================================
	#navigation 

	#==============================================================================
	
	def cleanup(self):
		RoverProcess.cleanup(self)
		# your cleanup code here. e.g. stopAllMotors()
	
	
if(os.name == "nt"):
	modulesList = ["plywoodbotProcess"]
else:
	modulesList = ["plywoodbotProcess"]
	
if __name__ == "__main__":

	processes = []
	i2cSem = multiprocessing.Semaphore(1)
	print "\nBUILD: Registering process subsribers...\n"
	
	if "plywoodbotProcess" in modulesList:
		process = plywoodbotProcess(
			downlink = system.getDownlink(), uplink = system.getUplink())
		processes.append(process)


	# start everything
	print "\nSTARTING: " + str([type(p).__name__ for p in processes]) + "\n"
	for process in processes:
		process.start()

	# wait until ctrl-C or error
	try:
		while True:
			time.sleep(60)
	except KeyboardInterrupt:
		print("\nSTOP: " + str([type(p).__name__ for p in processes]) + "\n")		
	finally:
		system.terminateState()