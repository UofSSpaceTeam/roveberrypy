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
from multiprocessing import Queue

class StateManager:
	class WorkerThread(Thread):
		## threading module automatically initializes and runs worker
		def __init__(self, uplink, subscriberMap, sem):
			Thread.__init__(self)
			self.uplink = uplink
			self.subscriberMap = subscriberMap
			self.stateSem = sem

		def run(self):
			while True:
				message = self.uplink.get()
				assert isinstance(message, dict)
				with self.stateSem:
					for key in message:
						self.notifySubscribers(key, message)

		## Helper to send data to the registered observers defined in main.py
		def notifySubscribers(self, key, message):
			if key in self.subscriberMap:
				for downlink in self.subscriberMap[key]:
					downlink.put(message)


	## Main state management functions
	def __init__(self):
		self.stateSem = BoundedSemaphore()
		self.subscriberMap = dict() # maps message names to
		self.downlinks = []

	def terminateState(self):
		#broken
		for queue in self.downlinks:
			queue.put({"quit":"True"})
		self.downlinks = []

	def dumpState(self):
		out = ""
		with self.stateSem:
			for key in self.state:
				out += str(key) + ":" + str(self.state[key]) + "\n"
		return out

	def getUplink(self):
		uplink = Queue()
		worker = StateManager.WorkerThread(
			uplink, self.subscriberMap, self.stateSem)
		worker.daemon = True
		worker.start()
		return uplink

	def addSubscriber(self, key, process):
		with self.stateSem:
			if key not in self.subscriberMap:
				self.subscriberMap[key] = list()
			if process.downlink not in self.subscriberMap[key]:
				self.subscriberMap[key].append(process.downlink)
			if process.downlink not in self.downlinks:
				self.downlinks.append(process.downlink)

	def removeSubscriber(self, key, process):
		with self.stateSem:
			if key not in self.subscriberMap:
				return # nothing to remove
			if process.downlink in self.subscriberMap[key]:
				self.subscriberMap[key].remove(process.downlink)

	def dumpSubscribers(self):
		out = ""
		with self.stateSem:
			for key in self.subscriberMap:
				out += str(key) + ":"
				out += str(len(self.subscriberMap[key])) + "\n"
		return out
