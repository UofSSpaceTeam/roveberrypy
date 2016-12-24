from .RoverProcess import RoverProcess

# Any libraries you need can be imported here. You almost always need time!
import time


class StateManagerTestProcess3(RoverProcess):
	def getSubscribed(self):
		return ["Test"]

	def setup(self, args):
		time.sleep(10)
		for msg_key in self.getSubscribed():
			self.subQueue.put([msg_key, self.name])
		
	
		
	
	def messageTrigger(self, message):
		
		if "Test" in message:
			print("Process 3 got: " + str(message["Test"]))
	
	