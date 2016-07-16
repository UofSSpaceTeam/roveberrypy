from RoverProcess import RoverProcess

# Any libraries you need can be imported here. You almost always need time!
import time


class ExampleProcess(RoverProcess):
	
	
	
	
	
	# Some blank space to write functions, classes, threads - whatever you need.
	# There are no restrictions - this is your own process!
	
	# See the tutorials on the wiki for things like basic threads and custom libraries.
	# 	< TO DO: INSTERT LINK TO THAT WIKI AND WRITE IT >
	
	
	
	
	
	# This is a tool to communicate with the main state manager at startup.
	# 	It returns a dictionary of lists for all the incoming (self) and outgoing (server) messages
	#	so that the StateManager knows who gets what message.
	# Just put the name of the message in the relevant list.
	def getSubscribed(self):		
		return {
				"self" : ["heartbeat"],
				"json" : ["TestData"],
				"can" : [],
				"web" : []
				}
	
	# This is run once to set up anything you need.
	# 	Hint: use the self object to store variables global to this process.
	# 	You can also take any args you need from the main startup as a dictionary:
	# 		self.something = args["something"]
	# 	This can be handy for sharing semaphores with other processes!
	def setup(self, args):
		self.someVariable = 42
	
	# This automatically loops forever.
	#	It is best to put a time.sleep(x) at the end. This makes sure that it 
	#	will always run at the same time, and will give other processes time to run too!
	# Use self.setShared() to send some variables to another process or server!
	def loop(self):
		self.setShared("TestData", time.time())
		time.sleep(1)
	
	# This runs every time a new message comes in.
	#	It is often handy to have an if statement for every type of message you expect
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		
		if "heartbeat" in message:
			print "got: " + str(message["heartbeat"])
	
	# This runs once at the end when the program shuts down.
	#	You can use this to do something like stop motors clean up open files 
	def cleanup(self):
		RoverProcess.cleanup(self)
