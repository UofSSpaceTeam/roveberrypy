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
from .RoverProcess import RoverProcess, RoverMessage
import threading
import time

import inspect

class Watchdog(Thread):
	def __init__(self, log, timeout=5):
		threading.Thread.__init__(self)
		self.state = {}
		self.counter = 0
		self.timeout = timeout
		self.log = log

	def run(self):
		while(True):
			self.log('Watchdog: Timer {} Guarding {}'.format(self.counter, self.state), level="DEBUG")

			if(self.counter == self.timeout):
				self.log('Watchdog timed out due to hung process: {}'.format(
				(process for process,running in self.state.items() if running==False).next()
				),
				level="CRITICAL")
			elif all(running == True for running in self.state.values()):
				self.counter = 0
			else:
				self.counter = self.counter + 1

			time.sleep(1)

	def pet(self, processName):
		self.state[processName] = True

	def guard(self, processName):
		self.state.update({processName:False})

	def patrol(self, timeout, processName):
		self.timeout = timeout
		self.log('Watchdog extended to {}s by process: {}'.format(timeout, processName))

class StateManager(RoverProcess):

	def setup(self, args):
		self.stateSem = BoundedSemaphore()
		self.subscriberMap = dict() # maps message names to list of processes

		self.watchdog = Watchdog(log=self.log)
		self.watchdog.start()

	def addSubscriber(self, key, pname):
		with self.stateSem:
			if key not in self.subscriberMap:
				self.subscriberMap[key] = list()
			if pname not in self.subscriberMap[key]:
				self.subscriberMap[key].append(pname)
			self.watchdog.guard(pname)

	def removeSubscriber(self, key, pname):
		with self.stateSem:
			if key in self.subscriberMap:
				if pname in self.subscriberMap[key]:
					self.subscriberMap[key].remove(pname)

	def terminateState(self):
		for pname in self.uplink:
			self.uplink[pname].put(RoverMessage("quit","True"))
 		self.uplink = dict()
		self.downlink.put(RoverMessage("quit","True"))

	def cleanup(self):
		try:
			quitReceiver = False
			self.log(self.__class__.__name__ + " shutting down")
			while(not quitReceiver):
				if (not quitReceiver) and self.receiver != threading.current_thread():
					quitReceiver = True
					self.receiver.quit = True
					self.receiver.join(0.01)  # receiver is blocked by call to queue.get()
				else: # cleanup was called from a message: cannot join current_thread
					self.quit = True
			self.log(self.__class__.__name__ + " shut down success!")
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
		if message.key == 'wd_pet':
			self.watchdog.pet(message.data)
		elif message.key == 'wd_extend':
			self.watchdog.patrol(message.data[0], message.data[1])
		elif message.key == 'subscribe':
			self.addSubscriber(message.data[0], message.data[1])
		elif message.key == 'unsubscribe':
			self.removeSubscriber(message.data[0], message.data[1])
		elif message.key in self.subscriberMap:
			for pname in self.subscriberMap[message.key]:
				if pname in self.uplink:
					self.uplink[pname].put(message)
