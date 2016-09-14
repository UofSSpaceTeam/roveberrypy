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

from multiprocessing import Process, BoundedSemaphore
import threading, sys

class RoverProcess(Process):
	class ReceiverThread(threading.Thread):
		def __init__(self, downlink, state, sem, parent):
			threading.Thread.__init__(self)
			self.downlink = downlink
			self._state = state
			self._stateSem = sem
			self._parent = parent
			self.quit = False
			self.daemon = True

		def run(self):
			while not self.quit:
				data = self.downlink.get()
				assert isinstance(data, dict)
				with self._stateSem:
					self._state.update(data)
				self._parent.messageTrigger(data)

	def __init__(self, **kwargs):
		Process.__init__(self)
		self.uplink = kwargs["uplink"]
		self.downlink = kwargs["downlink"]
		self._state = dict()
		self._stateSem = BoundedSemaphore()
		self._args = kwargs
		self.load = True
		self.receiver = RoverProcess.ReceiverThread(
			self.downlink, self._state, self._stateSem, self)

	def getSubscribed(self):
		pass

	def run(self):
		self.receiver.start()
		try:
			self.setup(self._args)
			while True:
				self.loop()
		except KeyboardInterrupt:
			self.cleanup()
			sys.exit(0)
		except:
			self.cleanup()
			raise

	def setup(self, args):
		pass

	def loop(self):
		pass

	def messageTrigger(self, message):
		if "quit" in message:
			print("Got cleanup")
			self.cleanup()
			sys.exit(0)

	def getShared(self, key):
		with self._stateSem:
			if key in self._state:
				return self._state[key]
			else:
				return None

	def setShared(self, key, value):
		with self._stateSem:
			self._state.update({key:value})
		self.uplink.put({key:value})

	def cleanup(self):
		self.receiver.quit = True
		self.receiver.join(0.25)  # receiver is blocked by call to queue.get()

