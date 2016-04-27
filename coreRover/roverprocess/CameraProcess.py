from RoverProcess import RoverProcess

import time

class CameraProcess(RoverProcess):

	def getSubscribed(self):
		# Returns a dictionary of lists for all the incoming (self) and outgoing (server) subscriptions
		return {
				"self" : [],
				"json" : [],
				"can" : [],
				"web" : []
				}

	def setup(self, args):
		pass
	
	def loop(self):
		#self.setShared("TestOut", "DEADBEEF")
		time.sleep(0.1)
		
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		#if "Test" in message:
		#	print message["Test"]
			
	def cleanup(self):
		RoverProcess.cleanup(self)
		
