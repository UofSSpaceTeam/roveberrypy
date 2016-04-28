from RoverProcess import RoverProcess

import time

class CameraProcess(RoverProcess):

	def getSubscribed(self):
		# Returns a dictionary of lists for all the incoming (self) and outgoing (server) subscriptions
		return {
				"self" : ["TestOut"],
				"json" : [],
				"can" : ["CameraUpDown", "CameraLeftRight"],
				"web" : []
				}

	def setup(self, args):
		pass
	
	def loop(self):
		self.setShared("CameraUpDown", str(1)) #control the position, value ranges between 1-90
		self.setShared("CameraLeftRight", str(50)) # control the speed, value ranges between 50-130, 90 -> stop
		time.sleep(1)
		self.setShared("CameraUpDown", str(45))
		self.setShared("CameraLeftRight", str(90))
		time.sleep(1)
		self.setShared("CameraUpDown", str(90))
		self.setShared("CameraLeftRight", str(130))
		time.sleep(1)
		time.sleep(0.1)
		
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "TestOut" in message:
			print message["TestOut"]
			
	def cleanup(self):
		RoverProcess.cleanup(self)
		
