
from RoverProcess import RoverProcess

# your imports go here. For example:
import time

class NavProcess(RoverProcess):
	
	def setup(self, args):
		# your setup code here
		self.run = False; 
		

	def loop(self):
		# your looping code here
	
		time.sleep(1)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		# your message handling here. for example:
		#if "exampleKey" in message:
		#	print "got: " + str(message["exampleKey"])
	
	
	def cleanup(self):
		RoverProcess.cleanup(self)
		# your cleanup code here. e.g. stopAllMotors()

	#-----------------------------------------------------------
	#navigation algorithm 
		
		
		
	#-------------------------------------------------------------
	#functions to interact with the rest of the system


	#allows the rover to be controlled by software
	#needs to be called before any other nav function can be ran
	def startNav(self):
		global run = True
		


	#sets the motors to the giving values
	#pre: startNav has to already be called
	#left: the value for the left side motors
	#right: the value for the right side motor
	def move(self, left, right):
		if (run):
			#add code to map values between 0 to 1
			
			#send message to left side motors
			self.setShared("inputOneLeftY", str(left))
			#send message to right side motors
			self.setShared("inputOneRightY", str(right))
		else
			print "error: Navigation mode has not started"


	#ends software control for the rover
	#start Nav has to be called again 
	def endNav(self):
		global run = False
		


 
