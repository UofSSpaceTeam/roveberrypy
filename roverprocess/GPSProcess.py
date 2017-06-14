from .RoverProcess import RoverProcess
from .GPS.Piksi import Piksi
from .GPS.sbp.navigation import *
from .GPS.sbp.system import *
from .GPS.sbp.observation import *

from threading import Thread
import time
import socket
import serial

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
								self._parent.publish('singlePointGPS', (msg.lat, msg.lon))
						time.sleep(1)
			except:
				self._parent.log("Bad serial port", "ERROR")

	def setup(self, args):
		receiver = GPSProcess.PiksiThread(self)
		receiver.daemon = True
		receiver.start()
