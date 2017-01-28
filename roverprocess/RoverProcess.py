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

from multiprocessing import Process, BoundedSemaphore, Queue, Manager
import threading
import sys
import time
import logging
from collections import namedtuple

# RoverMessage is a named tuple with key and data fields.
# msg = RoverMessage('test', [1, 2, 3])
# msg[0] == msg.key
# msg[1] == msg.data
RoverMessage = namedtuple('RoverMessage', ['key', 'data'])


class RoverProcess(Process):
	class ReceiverThread(threading.Thread):
		def __init__(self, downlink, parent):
			threading.Thread.__init__(self)
			self.downlink = downlink # MultiProcessing Queue.
			self._parent = parent # RoverProcess instance.
			self.quit = False
			self.daemon = True

		def run(self):
			while not self.quit:
				message = self.downlink.get() # Get subscribed message from multiprocessing queue.
				assert isinstance(message, RoverMessage) # Checking if the "message" is of type RoverMessage.
				if hasattr(self._parent, "on_" + message.key): # If message key has a function called on_*key*() in its RoverProcess instance...
					#...call trigger method, execute function.
					getattr(self._parent, "on_" + message.key)(message.data) 
				else: #... Otherwise call its message trigger.
					self._parent.messageTrigger(message)

	def __init__(self, **kwargs):
		Process.__init__(self)
		self._log = logging.getLogger(self.__class__.__name__)
		self.uplink = kwargs["uplink"]
		self.downlink = kwargs["downlink"]
		self.subscriptions = ["quit"]
		self._args = kwargs
		self.load = True
		self.quit = False
		self.receiver = RoverProcess.ReceiverThread(self.downlink, self)


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
		for msg_key in self.subscriptions:
			self.subscribe(msg_key)

	def loop(self):
		try:
			time.sleep(1)
		except KeyboardInterrupt:
			pass

	def messageTrigger(self, message):
		pass

	def on_quit(self, message):
		self.cleanup()
		sys.exit(0)

	def publish(self, key, value):
		self.uplink.put(RoverMessage(key, value))

	def cleanup(self):
		try:
			if self.receiver != threading.current_thread():
				logging.info(self.__class__.__name__ + " shutting down")
				self.receiver.quit = True
				self.receiver.join(0.01)  # receiver is blocked by call to queue.get()
			else: # cleanup was called from a message: cannot join current_thread
				self.quit = True
		except KeyboardInterrupt:
			pass

	def log(self, message, level="INFO"):
		level_lut = {"NOTSET":0, "DEBUG":10, "INFO":20,
				"WARNING":30, "ERROR":40, "CRITICAL":50}
		self._log.log(level_lut[level], message)

	def subscribe(self, key):
		if key not in self.subscriptions:
			self.subscriptions.append(key)
		self.publish("subscribe", [key, self.__class__.__name__])

	def unsubscribe(self, key):
		if key in self.subscriptions:
			self.subscriptions.remove(key)
		self.publish("unsubscribe", [key, self.__class__.__name__])


