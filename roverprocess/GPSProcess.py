from .RoverProcess import RoverProcess
from .GPS.Piksi import Piksi
from .GPS.sbp.navigation import *
from .GPS.sbp.system import *
from .GPS.sbp.observation import *

from threading import Thread
import time
import socket
import serial
from math import radians

class GPSPosition:
	# Earth's radius in metres
	RADIUS = 6371008.8

	def __init__(self, lat, lon):
		# lat an lon are assumed to be in radians
		self.lat = lat
		self.lon = lon

	def distance(self, them):
		''' Returns the distance to another GPSPositions on earth'''
		hav = lambda z: (1 - cos(z)) / 2   # haversine
		ahav = lambda z: 2 * asin(sqrt(z)) # inverse haversine

		d_lat = them.lat - self.lat
		d_lon = them.lon - self.lon

		z = (hav(d_lat)
				+ cos(self.lat) * cos(them.lat) * hav(d_lon))

		return GPSPosition.RADIUS * ahav(z)

	def bearing(self, them):
		''' Returns the bearing to another GPSPositions on earth'''
		d_lat = them.lat - self.lat
		d_lon = them.lon - self.lon

		y = sin(d_lon) * cos(them.lat)
		x = (cos(self.lat) * sin(them.lat)
				- sin(self.lat) * cos(them.lat) * cos(d_lat))

		return atan2(y, x)

class GPSProcess(RoverProcess):
	''' Polls a Piksi RTK GPS unit and publishes the
		GPS coordinate as a list:
		[latitude (degrees), longtitude (degrees)].
	'''

	class PiksiThread(Thread):
		''' Thread that waits on the Piksi GPS unit and
			publishes the coordinate.
			TODO: Can this just be put in the process its self?
		'''
		def __init__(self, parent):
			Thread.__init__(self)

			self._parent = parent
			# TODO: This conflicts with the USBServer...
			self.serial = "/dev/ttyUSB0"
			self.baud = 1000000
			self.addr = None
			self.port = None

		def run(self):
			#with Piksi(self.serial, self.baud, recv_addr=(self.addr, self.port)) as self.piksi:
			try:
				with Piksi(self.serial, self.baud) as self.piksi:
					while True:
						connected = self.piksi.connected()
						if not connected:
							self._parent.log("Rover piksi is not connected properly")
						else:
							self._parent.log("Rover piksi is connected", "WARNING")
							msg = self.piksi.poll(0x0201)
							if msg is not None:
								pos_msg = "lat:" + str(msg.lat) + ",lon:" + str(msg.lon)
								self._parent.log(pos_msg, "DEBUG")
								self._parent.publish('singlePointGPS',
										GPSPosition(radians(msg.lat), radians(msg.lon)))
						time.sleep(1)
			except:
				self._parent.log("Bad serial port", "ERROR")

	def setup(self, args):
		receiver = GPSProcess.PiksiThread(self)
		receiver.daemon = True
		receiver.start()
