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
		def __init__(self, uplink, state, observerMap, sem):
			Thread.__init__(self)
			self.uplink = uplink
			self.state = state
			self.observerMap = observerMap
			self.stateSem = sem

		def run(self):
			while True:
				data = self.uplink.get()
				assert isinstance(data, dict)
				with self.stateSem:
					self.state.update(data)
					for key in data:
						self.notifyObservers(key)

		## Helper to send data to the registered observers defined in main.py
		def notifyObservers(self, key):
			if key in self.observerMap:
				for downlink in self.observerMap[key]:
					downlink.put({key:self.state[key]})


	## Main state management functions
	def __init__(self):
		self.stateSem = BoundedSemaphore()
		self.state = dict()
		self.observerMap = dict()
		self.downlinks = []

	def terminateState(self):
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
			uplink, self.state, self.observerMap, self.stateSem)
		worker.daemon = True
		worker.start()
		return uplink

	def getDownlink(self):
		downlink = Queue()
		self.downlinks.append(downlink)
		return Queue()

	def addObserver(self, key, downlink):
		with self.stateSem:
			if key not in self.observerMap:
				self.observerMap[key] = list()
			if downlink not in self.observerMap[key]:
				self.observerMap[key].append(downlink)

	def dumpObservers(self):
		out = ""
		with self.stateSem:
			for key in self.observerMap:
				out += str(key) + ":"
				out += str(len(self.observerMap[key])) + "\n"
		return out
