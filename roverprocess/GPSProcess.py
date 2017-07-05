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
from statistics import mean

LOOP_PERIOD = 0.3 # How often we pusblish positions

class GPSPosition:
	# Earth's radius in metres
	RADIUS = 6371008.8

	def __init__(self, lat, lon, mode=0):
		# lat an lon are assumed to be in radians
		self.lat = lat
		self.lon = lon
		self.mode = mode # 0=SPP, 1=Float RTK, 2=Fixed RTK

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

	MSG_POS_LLH = 0x0201 # reports the absolute geodetic coordinate of the rover
	MSG_VEL_NED = 0x0205 # velocity in north, east, down coordinates

	NUM_SAMPLES = 10
	SAMPLE_RATE = 0.01 # seconds in between samples


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

		def run(self):
			try:
				with Piksi(self.serial, self.baud) as self.piksi:
					while True:
						connected = self.piksi.connected()
						if not connected:
							self._parent.log("Rover piksi is not connected properly", "ERROR")
						else:
							self._parent.log("Rover piksi is connected", "DEBUG")
							lats = []
							longs = []
							for i in range(GPSProcess.NUM_SAMPLES):
								# Take average of multiple samples.
								# Actually doesn't perform that well...
								msg = self.piksi.poll(GPSProcess.MSG_POS_LLH)
								if msg is not None:
									lats.append(msg.lat)
									longs.append(msg.lon)
									# self._parent.log("type: {}".format(msg.flags))
								time.sleep(GPSProcess.SAMPLE_RATE)
							if len(lats) > 1:
								self._parent.publish('singlePointGPS',
										GPSPosition(radians(mean(lats)), radians(mean(longs))))
							else:
								self._parent.log("Failed to take GPS averege", "WARNING")
							msg = self.piksi.poll(GPSProcess.MSG_VEL_NED)
							if msg is not None:
								self._parent.publish("GPSVelocity", [msg.n/1000, msg.e/1000])
						time.sleep(LOOP_PERIOD)
			except:
				raise
				self._parent.log("Bad serial port, or other failure", "ERROR")

	def setup(self, args):
		receiver = GPSProcess.PiksiThread(self)
		receiver.daemon = True
		receiver.start()
