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
from  multiprocessing import BoundedSemaphore

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
		self.DeviceList = []


	def messageTrigger(self, message):
		if message.key in self.subscriberMap:
			for port in self.subscriberMap[message.key]:
				with self.semList[port]:
					self.send_cmd(message, port)

	def send_cmd(self, message, port):
		""" Function for sending a message to a device.
			Override this method to handle the particular
			device communication standard you are using.

			Args:
				message: The rover message to send
				port (str): The port name device instance to send it to.
		"""
		pass

	def read_cmd(self, port):
		""" Function for reading messages from a device.
			Override this method to handle the particular
			device communication standard you are using.

			Args:
				port (str): Name of which device to read from.
		"""
		pass

	def getDevice(self, port):
		""" Returns a device instance of a port name
			Override this method to handle the particular
			device communication standard you are using.

			Args:
				port (str): Path to a particular instance of a device
		"""
		pass

	def getSubscription(self, port):
		""" Get the subscription(s) of a device.
			Override this method to handle the particular
			device communication standard you are using.

			Args:
				port (str): Path to a particular instance of a device
		"""
		pass

	def listenToDevice(self, **kwargs):
		""" Continualy read from a device and publish any received messages.

			Args:
				port (str): Path to a particular instance of a device
		"""
		with self.getDevice(kwargs['port']) as device:
			while not self.quit:
				msg = None
				try:
					with self.semList[kwargs['port']]:
						msg = self.read_cmd(device)
					if msg is not None:
						self.log(msg[0], "DEBUG")
						self.publish(msg[0], msg[1])
				except Exception as e:
					# failed to open port
					self.log("Read fail: " + str(e), "DEBUG")
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

	def reqSubscription(self, port):
		""" Request susbscriptions from a device.
		Subscribe to the message if we're not subscribed already.
		Also store the device for later. Finally, spin up a thread
		to listen for incomming messages from the device.

		Args:
			port (str): Path to a particular instance of a device
		"""
		with self.getDevice(port) as device:
			s = self.getSubscription(device)
			if not s:
				return # failed to get a good packet, abort
			if s not in self.subscriberMap:
				self.subscriberMap[s] = []
				self.subscribe(s)
			self.subscriberMap[s].append(port)
			self.DeviceList.append(port)
			self.semList[port] = BoundedSemaphore()
			self.spawnThread(self.listenToDevice, port=port)

	def cleanup(self):
		RoverProcess.cleanup(self)
		self.quit = True
		for thread in self.workers:
			try:
				thread.join(0.1)
			except KeyboardInterrupt:
				pass

