from RoverProcess import RoverProcess

import time

class CanExampleProcess(RoverProcess):

	def setup(self, args):
		pass
	
	def loop(self):
		pass
		
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "Test" in message:
			print message["Test"]
			
	def cleanup(self):
		RoverProcess.cleanup(self)
		
