from .RoverProcess import RoverProcess

# Any libraries you need can be imported here. You almost always need time!
import time


class StateManagerTestProcess1(RoverProcess):
	
	def loop(self):
		self.publish("Test", "StateManagerTest")
		time.sleep(1)
	
	