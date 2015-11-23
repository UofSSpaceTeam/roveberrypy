import time 
#uncomment when on pi
#import smbus
import pygame


class CommandType:
		setMotors = 0x00

class Command:
	def __init__(self):
		self.header = 0xF7
		self.type = 0x00
		self.d1 = 0x0000
		self.d2 = 0x0000
		self.csum = 0x00
		self.trailer = 0xF8
		
class plywoodbot:

	def __init__(self):
	
		#uncomment when on pi
		#self.i2c = smbus.SMBus(1)
		self.i2cAddress = 0x07   
		self.joyAxes = [0.0, 0.0]
		
		pygame.init()
		self.driveController = None
		if pygame.joystick.get_count() > 0:
			self.driveController = pygame.joystick.Joystick(0)
			self.driveController.init()
		else:
			print("No controller") 
	

	def loop(self):
		while True:
			pygame.event.pump()
			if self.driveController is not None:
				self.getContoller()
			
			self.setMotors(self.joyAxes)
			time.sleep(0.01)
		

	#==================================================================
	#controller 

	def getContoller(self):
		self.joyAxes[0] = self.driveController.get_axis(1)
		print "left joystick" , self.joyAxes[0]
		self.joyAxes[1] = self.driveController.get_axis(3)
		print "right joystick", self.joyAxes[1]
		
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
		#print "left input", command.d1
		command.d2 = int(speeds[1] * 255) # right
		#print "right input", command.d2
		
		self.sendCommand(command)
		
	def sendCommand(self, command):
		command.csum = (command.type + command.d1 + command.d2) % 256
		try:
			print("sending command to motors")
			#uncomment when on pi
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
		
	#=============================================================================
	#navigation 

#=================================================================================
#main starts here 

if __name__ == "__main__":

	plybot = plywoodbot()
	plybot.loop() 	
	
	
	