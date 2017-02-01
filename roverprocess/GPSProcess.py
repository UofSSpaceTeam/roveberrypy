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
	class PiksiThread(Thread):
		def __init__(self, parent):
			Thread.__init__(self)

			self._parent = parent
			self.serial = "/dev/ttyUSB0"
			self.baud = 1000000
			self.addr = None
			self.port = None

		def run(self):
			#with Piksi(self.serial, self.baud, recv_addr=(self.addr, self.port)) as self.piksi:
			with Piksi(self.serial, self.baud) as self.piksi:
				while True:
					connected = self.piksi.connected()
					if not connected:
						print("Rover piksi is not connected properly")
					else:
						print("Rover piksi is connected")
						msg = self.piksi.poll(0x0201)
						if msg is not None:
							print("location")
							pos_msg = "lat:" + str(msg.lat) + ",lon:" + str(msg.lon)
							print(pos_msg)
							self._parent.messageTrigger({"pos":pos_msg})

					time.sleep(1)

	def setup(self, args):
		receiver = GPSProcess.PiksiThread(self)
		receiver.daemon = True
		receiver.start()
