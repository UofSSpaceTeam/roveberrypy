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

from threading import Thread, BoundedSemaphore
from multiprocessing import Process, Queue
from .RoverProcess import RoverProcess
import threading

class StateManager(RoverProcess):

	def setup(self, args):
		self.stateSem = BoundedSemaphore()
		self.subscriberMap = dict() # maps message names to list of processes

	def addSubscriber(self, key, pname):
		with self.stateSem:
			if key not in self.subscriberMap:
				self.subscriberMap[key] = list()
			if pname not in self.subscriberMap[key]:
				self.subscriberMap[key].append(pname)

	def terminateState(self):
		for pname in self.uplink:
			self.uplink[pname].put({"quit":"True"})
		self.uplink = dict()
		self.downlink.put({"quit":"True"})

	def cleanup(self):
		try:
			quitReceiver = False
			print(self.__class__.__name__ + " shutting down")
			while(not quitReceiver):
				if (not quitReceiver) and self.receiver != threading.current_thread():
					quitReceiver = True
					self.receiver.quit = True
					self.receiver.join(0.01)  # receiver is blocked by call to queue.get()
				else: # cleanup was called from a message: cannot join current_thread
					self.quit = True
			print(self.__class__.__name__ + " shut down success!")
		except KeyboardInterrupt:
			pass

	def dumpSubscribers(self):
		out = ""
		with self.stateSem:
			for key in self.subscriberMap:
				out += str(key) + ":"
				out += str(len(self.subscriberMap[key])) + "\n"
		return out

	def messageTrigger(self, message):
		for key in message:
			if key == "subscribe":
				self.addSubscriber(message["subscribe"][0], message["subscribe"][1])
			elif key in self.subscriberMap:
				for pname in self.subscriberMap[key]:
					if pname in self.uplink:
						self.uplink[pname].put(message)


