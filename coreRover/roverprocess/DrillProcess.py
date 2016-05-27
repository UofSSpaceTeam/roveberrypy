from RoverProcess import RoverProcess

import time

class DrillProcess(RoverProcess):

	def getSubscribed(self):
		# Returns a dictionary of lists for all the incoming (self) and outgoing (server) subscriptions
		return {
				"self" : [],
				"json" : [],
				"can" : ["DrillMotor", "ElevMotor", "Moisture", "x"],
				"web" : []
				}

	def setup(self, args):
		pass
	
	def loop(self):
		self.setShared("DrillMotor", str(0)) 
		time.sleep(1)
		self.setShared("ElevMotor", str(0)) 
		time.sleep(1)
		self.setShared("DrillMotor", str(-5)) 
		time.sleep(1)
		self.setShared("ElevMotor", str(-5)) 
		time.sleep(1)
		self.setShared("DrillMotor", str(-10)) 
		time.sleep(1)
		self.setShared("ElevMotor", str(-10)) 
		time.sleep(1)
		self.setShared("DrillMotor", str(0)) 
		time.sleep(1)
		self.setShared("ElevMotor", str(0)) 
		time.sleep(1)
		self.setShared("DrillMotor", str(5)) 
		time.sleep(1)
		self.setShared("ElevMotor", str(5)) 
		time.sleep(1)
		self.setShared("DrillMotor", str(10)) 
		time.sleep(1)
		self.setShared("ElevMotor", str(10)) 
		time.sleep(1)
		time.sleep(0.1)
		
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "Moisture" in message:
			print "Moisture: " + message["Moisture"]
		if "x" in message:
			print "x: " + message["x"]
			
	def cleanup(self):
		RoverProcess.cleanup(self)
		
