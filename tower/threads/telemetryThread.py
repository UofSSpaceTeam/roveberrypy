import threading
from Queue import Queue
import time
#from RPIO import PWM as pwm
import serial
from unicodeConvert import convert

class telemetryThread(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.name = "telemetryThread"
		self.parent = parent
		self.mailbox = Queue()
		self.gps = serial.Serial("/dev/ttyAMA0", bytesize = 8, parity = 'N',
			stopbits = 1)
		self.gps.baudrate = 9600
		self.gps.timeout = 0.2

	def run(self):
		while True:
			location = self.readGPS()
			if location != None:
				self.parent.commThread.mailbox.put({"towerGPS":location})
			time.sleep(5)
	
	def readGPS(self):
		rawData = self.gps.read(self.gps.inWaiting())
		dataStart = rawData.find("GGA")
		if dataStart != -1:	# found start of valid sentence
			dataEnd = min(dataStart + 70, len(rawData) - dataStart - 2)
			data = rawData[dataStart:dataEnd]
			values = data.split(",")
			if len(values) > 9:
				latitude = float(values[2][:2])
				latmin = float(values[2][2:])
				longitude = -1 * float(values[4][:3])
				lonmin = float(values[4][3:])
				hdop = float(values[8])
				altitude = float(values[9])
				if latitude > 0:
					latitude += latmin / 60.0
				else:
					latitude -= latmin / 60.0
				if longitude > 0:
					longitude += lonmin / 60.0
				else:
					longitude -= lonmin / 60.0
				return (latitude, longitude)
		return None

