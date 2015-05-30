import threading
from Queue import Queue
import serial

class TelemetryThread(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "Telemetry"
		self.mailbox = Queue()
		self.port = serial.Serial("/dev/ttyAMA0", 9600)

	def run(self):
		while True:
			while self.port.read() != '@':
				pass
			inChar = self.port.read()
			while inChar != '$':
				inData += inChar
				inChar = self.port.read()
			try:
				inData = inData.split(',')
				lat = float(inData[0])
				lon = float(inData[1])
				speed = int(float(inData[2]) * 60)
				heading = int(float(inData[3]))
			except:
			#	pass
				raise
			else:
				msg = {"roverGPS":(lat, lon, speed, heading)}
				self.parent.commThread.mailbox.put(msg)

