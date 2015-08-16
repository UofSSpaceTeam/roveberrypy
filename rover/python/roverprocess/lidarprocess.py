from roverprocess import RoverProcess

import serial

class LidarProcess(RoverProcess):
	def setup(self, args):
		self.serial = serial.Serial(serial.Serial(port=args["serialPort"],
			baudrate=57600)

	def loop(self):
		self.receiveData()

	def receiveData(self)
		# reads arbitrary (integer) sensor data into shared state
		# format is <key:value>
		try:
			inData = self.serial.readline(eol=">")
			openTag = inData.find("<")
			if openTag == -1:
				return
			inData = inData[openTag:]
			print inData
			colon = inData.find(":")
			if colon == -1:
				return
			key = inData[1:colon]
			value = inData[(colon + 1):-1]
			self.setShared(key, int(value))
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
