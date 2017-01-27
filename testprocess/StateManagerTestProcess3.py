from roverprocess.RoverProcess import RoverProcess

# Any libraries you need can be imported here. You almost always need time!
import time


class StateManagerTestProcess3(RoverProcess):
	def setup(self, args):
		sublist = ["Test"]
		time.sleep(5)
		for msg_key in sublist:
			self.subscribe(msg_key)
		time.sleep(5)
		for msg_key in sublist:
			self.unsubscribe(msg_key)

	def messageTrigger(self, message):

		if "Test" in message:
			self.log("Process 3 got: " + str(message["Test"]))


