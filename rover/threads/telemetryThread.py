import threading
from Queue import Queue
import serial

class TelemetryThread(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "Telemetry"
		self.mailbox = Queue()
		self.port = serial.Serial("/dev/ttyAMA0", 57600)
		self.messageElements = 21
				
	def run(self):
		while True:
			data = self.getSerialData()
			if data is not None:
				msg = {"roverGPS":(data["lat"], data["lon"], data["speed"],
					data["gps_heading"])}
				self.parent.commThread.mailbox.put(msg)
								
	def getSerialData(self):
		inData = ""
		outData = {}
		# wait for message start
		while self.port.read() != "#":
			pass
		# wait for message end
		inChar = self.port.read()
		while inChar != "$":
			inData += inChar
			inChar = self.port.read()
		# parse message
		print inData
		inData = inData.split();
		if len(inData) != self.messageElements:
			return None
		outData["pitch"] = float(inData[0])
		outData["roll"] = float(inData[1])
		outData["gx"] = float(inData[2])
		outData["gy"] = float(inData[3])
		outData["gz"] = float(inData[4])
		outData["ax"] = float(inData[5])
		outData["ay"] = float(inData[6])
		outData["az"] = float(inData[7])
		outData["heading"] = int(inData[8])
		outData["aroll"] = float(inData[9])
		outData["apitch"] = float(inData[10])
		outData["lat"] = float(inData[11])
		outData["lon"] = float(inData[12])
		outData["speed"] = float(inData[13]) / 60
		outData["alt"] = int(inData[14])
		outData["gps_heading"] = int(inData[15])
		outData["date"] = inData[16]
		outData["time"] = inData[17]
		outData["vout"] = float(inData[18])
		outData["isense"] = float(inData[19])
		return outData

