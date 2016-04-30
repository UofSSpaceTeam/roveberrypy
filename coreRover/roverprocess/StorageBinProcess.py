from RoverProcess import RoverProcess

import time

class StorageBinProcess(RoverProcess):

	def getSubscribed(self):
		# Returns a dictionary of lists for all the incoming (self) and outgoing (server) subscriptions
		return {
				"self" : [],
				"json" : [],
				"can" : ["Open", "Close"],
				"web" : []
				}

	def setup(self, args):
		pass
	
	def loop(self):
		self.setShared("Open", str(1))
		time.sleep(1)
		self.setShared("Close", str(1)) 
		time.sleep(1)
		self.setShared("Open", str(2))
		time.sleep(1)
		self.setShared("Close", str(2))
		time.sleep(1)
		self.setShared("Open", str(3))
		time.sleep(1)
		self.setShared("Close", str(3))
		time.sleep(1)
		time.sleep(0.1)
		
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		#if "TestOut" in message:
		#	print message["TestOut"]
			
	def cleanup(self):
		RoverProcess.cleanup(self)