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

class StateManager(RoverProcess):
	"""  Handles the IPC mechanism for the rover software.

	The StateManager is somewhat unique, in that it must
	allways be enabled. Whenever a RoverProcess publishes
	a message, the message goes to the StateManager,
	and the StateManager decides where to push the message to next.
	"""

	def setup(self, args):
		self.stateSem = BoundedSemaphore()
		self.subscriberMap = dict() # maps message names to list of processes

	def addSubscriber(self, key, pname):
		""" Register a process as a subscriber to a *key*.

			Args:
				key (str): The key to subscribe to.
				pname (str): The name of the process.
		"""
		with self.stateSem:
			if key not in self.subscriberMap:
				self.subscriberMap[key] = list()
			if pname not in self.subscriberMap[key]:
				self.subscriberMap[key].append(pname)

	def removeSubscriber(self, key, pname):
		""" Remove a process from a subscription.

			Args:
				key (str): The key to unsubscribe from.
				pname (str): The name of the process to unsubscribe.
		"""
		with self.stateSem:
			if key in self.subscriberMap:
				if pname in self.subscriberMap[key]:
					self.subscriberMap[key].remove(pname)

	def terminateState(self):
		""" Send the quit message to all processes handled by the StateManager."""
		for pname in self.uplink:
			self.uplink[pname].put(RoverMessage("quit","True"))
		self.uplink = dict()
		self.downlink.put(RoverMessage("quit","True"))

	def cleanup(self):
		"""From RoverProcess, shut down the StateManager."""
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
		""" Returns a string of the subscriptions in the system. Legacy"""
		out = ""
		with self.stateSem:
			for key in self.subscriberMap:
				out += str(key) + ":"
				out += str(len(self.subscriberMap[key])) + "\n"
		return out

	def messageTrigger(self, message):
		''' From RoverProcess, called when a message comes in.

		If the mesage is "subscribe", subscribe that process to the
		desired key. If the message is "unsubscribe", remove that
		process from the key subscription.
		Otherwise, forward the incomming message to all processes
		that are subscribed to that key.
		'''
		if message.key == 'subscribe':
			self.addSubscriber(message.data[0], message.data[1])
		elif message.key == 'unsubscribe':
			self.removeSubscriber(message.data[0], message.data[1])
		elif message.key in self.subscriberMap:
			for pname in self.subscriberMap[message.key]:
				if pname in self.uplink:
					self.uplink[pname].put(message)


