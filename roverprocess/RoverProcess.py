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

RoverMessage = namedtuple('RoverMessage', ['key', 'data'])
''' RoverMessage is a named tuple with key and data fields.  '''


class RoverProcess(Process):
	""" RoverProcesses are modules that handle functionality of one component of the rover.
		RoverProcesses somewhat emulate an Arduino, in that there is a setup and loop function.
		They also provide an interprocess communication mechanism based on the publisher/subscriber
		design pattern.
	"""

	class ReceiverThread(threading.Thread):
		""" ReceiverThread listens for incoming messages."""
		def __init__(self, downlink, parent):
			""" Constructor.

				Args:
					downlink (multiprocessing.Queue): The incomming message (multiprocessing) queue of the parent rover process.
					parent (roverprocess.RoverProcess.RoverProcess): instance of the RoverProcess
			"""
			threading.Thread.__init__(self)
			self.downlink = downlink
			self._parent = parent
			self.quit = False
			self.daemon = True

		def run(self):
			""" Run in a new thread. Loops until system shutdown.
				Waits for a new message to come onto the downlink queue,
				and if the RoverProcess has a method called on_<key>(), where
				<key> is the key of the incomming RoverMessage, that method is called
				with the message's data as a parameter. Otherwise, the RoverProcess's
				messageTrigger method is called with the message as a parameter.
			"""
			while not self.quit:
				message = self.downlink.get() # BLOCKING: Get subscribed message from multiprocessing queue.
				assert isinstance(message, RoverMessage) # Ensure message is a RoverMessasge
				if hasattr(self._parent, "on_" + message.key): # If the RoverProcess instance  has a function called on_<key>()...
					getattr(self._parent, "on_" + message.key)(message.data)
				else:
					self._parent.messageTrigger(message)

	def __init__(self, **kwargs):
		""" Constructor, called in main.py automatically, don't override this through inheritance.

			Args:
				uplink (multiprocessing.Queue): queue for outgoing messages
				downlink (multiprocessing.Queue): queue for incomming messages
		"""
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
		""" This is method is what runs in a new process.
		First the receiver thread is started, then the setup method is
		called, and finally the loop method is run in an infinite while loop.
		"""
		self.receiver.start()
		try:
			self.setup(self._args)

			while not self.quit:
				try:
					# For any process that is not the state manager, make sure to
					# send an notification that it is running at the start of each loop
					if(self.__class__.__name__ is not 'StateManager'):
						self.watchdogPet()
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
		""" Treated as a pseudo constructor, initialization of the process.
			Arguments from the real constructor are passed in as <args>
		"""
		for msg_key in self.subscriptions:
			self.subscribe(msg_key)

	def loop(self):
		""" Runs continually during the lifetime of the system.
			Defaults to sleep for one second.
		"""
		try:
			time.sleep(1)
		except KeyboardInterrupt:
			pass

	def messageTrigger(self, message):
		""" Generic message handler.
			Typically, you want to use an if/else statement on the
			message key and do different things depending on the key.

			Args:
				message (RoverMessage): A single rovermessage that was received.
		"""
		pass

	def on_quit(self, message):
		''' Callback for the "quit" message.
			Calls cleanup() and exits the process.
		'''
		self.cleanup()
		sys.exit(0)

	def publish(self, key, value):
		""" Publishes a new RoverMessage to the rover system.

			Args:
				key (str): An identifier for the message.
				value: The actual contents/data of the message.
		"""
		self.uplink.put(RoverMessage(key, value))

	def cleanup(self):
		""" Acts like a deconstructor.
			Shuts down the receiver thread. If you override this method, be sure
			to call RoverProcess.cleanup() to ensure everything shuts down properly.
		"""
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
		''' Logs a message.
			Messages are logged to the console and a file, depending how things
			are setup in main.py.

			Args:
				message: A string to log, can also be an integer, float etc.
				level (str): A string representing the log level as defined in the standard python logging module.\
						Can be one of: "NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
		'''
		level_lut = {"NOTSET":0, "DEBUG":10, "INFO":20,
				"WARNING":30, "ERROR":40, "CRITICAL":50}
		self._log.log(level_lut[level], message)

	def subscribe(self, key):
		""" Subscribe this RoverProcess to messages identified by <key>

			Args:
				key (str): An identifier for the key you want to subscribe to.
		"""
		if key not in self.subscriptions:
			self.subscriptions.append(key)
		self.publish("subscribe", [key, self.__class__.__name__])

	def unsubscribe(self, key):
		""" Un-subscribe this RoverProcess to messages identified by <key>

			Args:
				key (str): An identifier for the key you want to un-subscribe from.
		"""
		if key in self.subscriptions:
			self.subscriptions.remove(key)
		self.publish("unsubscribe", [key, self.__class__.__name__])

	# Watchdog Functions
	def watchdogPet(self):
		self.publish('wd_pet', self.__class__.__name__)

	def watchdogExtend(self, timeout):
		self.publish('wd_extend', [timeout, self.__class__.__name__ ])

	def watchdogReset(self):
		self.publish('wd_reset', [self.__class__.__name__ ])
