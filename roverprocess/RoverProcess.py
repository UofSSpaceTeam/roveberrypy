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

from multiprocessing import Process, BoundedSemaphore, Queue
import threading
import sys
import time

class RoverProcess(Process):
	class ReceiverThread(threading.Thread):
		def __init__(self, downlink, parent):
			threading.Thread.__init__(self)
			self.downlink = downlink
			self._parent = parent
			self.quit = False
			self.daemon = True

		def run(self):
			while not self.quit:
				data = self.downlink.get()
				assert isinstance(data, dict)
				for key in data.keys():
					if hasattr(self._parent, "on_" + key):
						#call trigger method
						getattr(self._parent, "on_" + key)(data[key])
					else:
						self._parent.messageTrigger(data)

	def __init__(self, **kwargs):
		Process.__init__(self)
		self.manager = kwargs["manager"]
		self.uplink = self.manager.getUplink()
		self.downlink = Queue()
		self._args = kwargs
		self.load = True
		self.quit = False
		self.receiver = RoverProcess.ReceiverThread(self.downlink, self)

	def getSubscribed(self):
		return ["quit"]

	def run(self):
		self.receiver.start()
		try:
			self.setup(self._args)
			while not self.quit:
				try:
					self.loop()
				except KeyboardInterrupt:
					self.quit = True
			self.cleanup()
		except KeyboardInterrupt:
			self.quit = True
			self.cleanup()
		except:
			self.cleanup()
			raise

	def setup(self, args):
		pass

	def loop(self):
		pass

	def messageTrigger(self, message):
		pass

	def on_quit(self, message):
		self.cleanup()
		sys.exit(0)

	def publish(self, key, value):
		self.uplink.put({key:value})

	def cleanup(self):
		if self.receiver != threading.current_thread():
			print(self.__class__.__name__ + " shutting down")
			self.receiver.quit = True
			self.receiver.join(0.01)  # receiver is blocked by call to queue.get()
		else: # cleanup was called from a message: cannot join current_thread
			self.quit = True

