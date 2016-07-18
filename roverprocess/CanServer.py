# Copyright 2016 University of Saskatchewan Space Design Team Licensed under the
# Educational Community License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may
# obtain a copy of the License at
#
# https://opensource.org/licenses/ecl2.php
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing
# permissions and limitations under the License.

from RoverProcess import RoverProcess

import time
from threading import Thread
from multiprocessing import BoundedSemaphore
from collections import defaultdict
import can

class CanServer(RoverProcess):

	class ListenThread(Thread):
		def __init__(self, bus, uplink, parent):
			Thread.__init__(self)
			self.bus = bus
			self.uplink = uplink
			self.parent = parent

		def run(self):
			while True:
				for msg in self.bus:
					#print msg.arbitration_id
					data = {self.parent.CanIdLUT[msg.arbitration_id] : str(msg.data)}
					if isinstance(data, dict):
						self.uplink.put(data)

	def setup(self, args):
		self.sendPeriod = args["sendPeriod"]
		self.bus = can.interface.Bus("can0", bustype="socketcan")
		self.data = {}
		self.dataSem = BoundedSemaphore()
		receiver = CanServer.ListenThread(self.bus, self.uplink, self)
		receiver.daemon = True
		receiver.start()

		## LUT to convert CAN Arbitration IDs to Names
		# Note that the lower the ID, the higher priority it has on the bus!
		# If unknown ids come through they are given the name unknown and vice versa with unknown names
		self.CanIdLUT = {
		546L  : "Test",
		547L  : "TestOut",
		1000L : "unknown",
		300L  : "CameraUpDown",
		301L  : "CameraLeftRight",
		400L  : "Open",
		401L  : "Close",
		769L  : "769",
		1L    : "1",
		257   : "257",
		0x901L : "m1Stats",
        500L : "DrillMotor",
		501L : "ElevMotor",
		502L : "Moisture",
		503L : "temperature"
		}
		self.CanIdRLUT = {v: k for k, v in self.CanIdLUT.items()} #reverse lookup
		self.CanIdLUT = defaultdict(lambda: "unknown", self.CanIdLUT)

		self.load = False

	def loop(self):
		if self.data:
			with self.dataSem:
				for key, value in self.data.iteritems():
					canId = self.CanIdRLUT[key]
					canData = bytearray()
					canData.extend(value)
					#print "CAN Message: ", canId, canData
					msg = can.Message(data=canData, arbitration_id=canId, extended_id=True)
					#print "CAN DATA: ", msg
					self.bus.send(msg)
				self.data = {}
		time.sleep(self.sendPeriod)

	def messageTrigger(self, message):
		# Prevent threads from triggering before server has started
		while self.load: time.sleep(0.001)
		RoverProcess.messageTrigger(self, message)
		with self.dataSem:
			self.data.update(message)

	def cleanup(self):
		self.bus.shutdown()
		RoverProcess.cleanup(self)
