from roverprocess import RoverProcess

import serial

class LidarProcess(RoverProcess):
	def setup(self, args):
		self.topData = []
		self.bottomData = []
		self.count = 
		self.serial = serial.Serial(serial.Serial(port=args["serialPort"],
			baudrate=57600)

	def loop(self):
		self.receiveData()

	def receiveData(self)
		# format is <top bottom count direction>
		try:
			inData = self.serial.readline(eol=">")
			openTag = inData.find("<")
			if openTag == -1:
				return
			inData = inData[openTag:-1]
			inData = inData.split()
			self.direction = int(inData[3])
			if int(inData[2]) == 0:
				if self.direction:
					self.topData.reverse()
					self.bottomData.reverse()
				self.setShared("lidarTop", str(self.topData))
				self.setShared("lidarBottom", str(self.bottomData))
				self.setShared("lidarCount", int(self.count))
			self.count = int(inData[2])
			self.topData.insert(self.count, inData[0])
			self.bottomData.insert(self.count, inData[1])
		except:
			pass

	def sendCommand(self, key, value)
		serial.write("<" + key + ":" + str(value) + ">")

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "lidarHeartbeat" in message:
			self.setShared("lidarHeartbeat", True)
		if "scanRate" in message:
			self.sendCommand("scanRate", int(message["scanRate"] * 10))
	
	def cleanup(self):
		RoverProcess.cleanup(self)
		self.serial.close()
