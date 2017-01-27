from roverprocess.RoverProcess import RoverProcess

# Any libraries you need can be imported here. You almost always need time!
import time


class StateManagerTestProcess2(RoverProcess):
	def setup(self, args):
		self.subscribe("Test")

	def messageTrigger(self, message):

		if "Test" in message:
			self.log("Process 2 got: " + str(message["Test"]))


