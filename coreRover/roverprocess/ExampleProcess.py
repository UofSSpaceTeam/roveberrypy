from RoverProcess import RoverProcess

# your imports go here. For example:
import time

class ExampleProcess(RoverProcess):
	
	# helper classes go here if you want any
	
	def getSubscribed(self):
		# Returns a dictionary of lists for all the incoming (self) and outgoing (server) subscriptions
		return {
				"self" : ["heartbeat"],
				"json" : ["exampleTime"],
				"can" : [],
				"web" : ["TestData"]
				}
	
	def setup(self, args):
		# your setup code here. examples:
		# self.something = args["something"]
		self.someVariable = 42
	
	def loop(self):
		# your looping code here. for example:
		self.setShared("exampleTime", time.time())
		self.setShared("TestData", time.time())
		time.sleep(1)
	
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		# your message handling here. for example:
		if "heartbeat" in message:
			print "got: " + str(message["heartbeat"])
	
	def cleanup(self):
		RoverProcess.cleanup(self)
		# your cleanup code here. e.g. stopAllMotors()
	
	# additional functions go here

