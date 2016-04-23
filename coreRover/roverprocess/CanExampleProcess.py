from RoverProcess import RoverProcess

import time

class CanExampleProcess(RoverProcess):

	def setup(self, args):
		pass
	
	def loop(self):
		self.setShared("TestOut", "DEADBEEF")
		time.sleep(0.1)
		
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "Test" in message:
			print message["Test"]
			
	def cleanup(self):
		RoverProcess.cleanup(self)
		
