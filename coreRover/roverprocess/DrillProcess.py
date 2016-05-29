from RoverProcess import RoverProcess

import time

class DrillProcess(RoverProcess):
	def __init__(self, **kwargs):
		RoverProcess.__init__(self, **kwargs)
		self.drillSpeed = 0
		self.elevSpeed = 0

	def getSubscribed(self):
		# Returns a dictionary of lists for all the incoming (self) and outgoing (server) subscriptions
		return {
				"self" : ["Moisture", "temperature", "drillControls"],
				"json" : [],
				"can" : ["DrillMotor", "ElevMotor"],
				"web" : []
				}

	def setup(self, args):
		pass
	
	def loop(self):
		self.setShared("DrillMotor", str(self.drillSpeed)) 
		self.setShared("ElevMotor", str(self.elevSpeed)) 
		time.sleep(0.1)
		 
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "Moisture" in message:
			print "Moisture: " + message["Moisture"]
		if "temperature" in message:
			print "temperature: " + message["temperature"]
		if "drillControls" in message:
			data = message["drillControls"] #message: [drillSpeed, elevbutton(-1: down, 0: not pressed, 1: up)]
			print data
			self.drillSpeed = data[0]
			if data[1] == -1:
				if self.elevSpeed == 0:
					self.elevSpeed = -30
				elif self.elevSpeed < 40 and self.elevSpeed > 0:
					self.elevSpeed = 0
				elif self.elevSpeed > -255:
					self.elevSpeed = self.elevSpeed - 1
			elif data[1] == 1:
				if self.elevSpeed == 0:
					self.elevSpeed = 40
				elif self.elevSpeed > -30 and self.elevSpeed < 0:
					self.elevSpeed = 0
				elif self.elevSpeed < 255:
					self.elevSpeed = self.elevSpeed + 1
				
			
			
	def cleanup(self):
		RoverProcess.cleanup(self)
		
