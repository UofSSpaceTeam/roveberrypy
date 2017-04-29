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

from .RoverProcess import RoverProcess

import time
import sys
from threading import Thread

class RoverServer(RoverProcess):
	"""Just a RoverProcess that adds an easy way to run a method in a new thread.

	This just prevents you from having to create a new class
	that inherits from Thread for every new thread you want to make.
	"""

	class WorkerThread(Thread):
		"""New thread that runs a given method/funciton."""
		def __init__(self, function, **kwargs):
			"""Initialize a thread to run a function.

				Args:
					function: The function to run.
					kwargs: arguments to the function.
			"""
			Thread.__init__(self)
			self.kwargs = kwargs
			self.function = function
			self.daemon = True

		def run(self):
			""" Run the thread, called by Thread.start()"""
			try:
				# Just call the function we were initialized with
				self.function(**self.kwargs)
			except KeyboardInterrupt:
				pass

	def __init__(self, **kwargs):
		RoverProcess.__init__(self, downlink=kwargs["downlink"],
				uplink=kwargs["uplink"])
		self.workers = []
		self.subscriberMap = {}
		self.semList = {}
		

	def messageTrigger(self, message):
		if message.key in self.subscriberMap:
			for device in self.subscriberMap[message.key]:
				self.send_cmd(message, device)

	def send_cmd(self, message, device):
		""" Function for sending a message to a device.
			Override this method to implement proper sending
			of data over whatever standard you are using.

			Args:
				message: The rover message to send
				device: The device instance to send it to.
		"""
		pass

	def read_cmd(self, device):
		""" Function for reading messages from a device.
			Override this method to implement proper sending
			of data over whatever standard you are using.
			
			Args:
				device: name of which device to read from.
				in your overriden version, use this in a with statement.
		"""
		pass

	def listenToDevice(self, **kwargs):
		while not self.quit:
			try:
				msg = self.read_cmd(kwargs['port'])
				if msg is not None:
					self.log(msg[0], "DEBUG")
					self.publish(msg[0], msg[1])
			except:
				# failed to open port
				self.log("Read fail", "DEBUG")
				pass
			time.sleep(0.005)

	def spawnThread(self, function, **kwargs):
		"""Spawns a new thread with the given function.


		Functions need the following prototype::

			def func(**kwargs):
				...

		including ``self`` if necessary.

		Args:
			function: The function/method to run in a new thread
			kwargs: The arguments to pass into the function. (This is a multi parameter call)
		"""
		new_thread = RoverServer.WorkerThread(function, **kwargs)
		self.workers.append(new_thread)
		new_thread.start()
	
	def getSubscription(self, port):
		pass
	
	
	def reqSubscription(self, port):
		""" Request susbscriptions from a device.

		Subscribe to the message if we're not subscribed already.
		Also store the device for later. Finally, spin up a thread
		to listen for incomming messages from the device.
		"""
		s = self.getSubscription(port)
		if not s:
			return # failed to get a good packet, abort
		if s not in self.subscriberMap:
			self.subscriberMap[s] = []
			self.subscribe(s)
		self.subscriberMap[s].append(port.device)
		self.DeviceList.append(port.device)
		#self.semList[port.device] = BoundedSemaphore()
		
		self.spawnThread(self.listenToDevice, port=port.device)

	def cleanup(self):
		RoverProcess.cleanup(self)
		self.quit = True
		for thread in self.workers:
			try:
				thread.join(0.1)
			except KeyboardInterrupt:
				pass

