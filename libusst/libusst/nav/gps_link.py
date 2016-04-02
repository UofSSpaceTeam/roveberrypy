"""
Author: 
	Liam Bindle <liam.bindle@gmail.com>

Description:
	This class provides a link with a Piksi GPS module. Most of it is redundant
	but is here to provide a cleaner and easier to use interface.
	
Progress:
	This module is still under development.
	
Dependancies:
	This module requires libsbp branch v0.49.
"""

from libusst.external.sbp.client.drivers.pyserial_driver import PySerialDriver
from libusst.external.sbp.client.handler import Handler
from libusst.external.sbp.settings import *
from libusst.external.sbp.navigation import *
import time

import piksi_settings
import logging

class GPSLink(object):
	"""
	GPSLink
	
	The :class:`GPSLink` class provides a link to a Piksi GPS module.
	
	Paramaters
	-----------
	verbose : bool
		Print additional debug information as well as add additional 
		safe-guards.
	"""
	def __init__(self, verbose=False):
		self._verbose = verbose
		self.log = logging.getLogger(__name__)
		self.log.debug("GPSLink instance created.")
	
	def __del__(self):
		self.close()
		
	def __exit__(self):
		self.close()
	
	def open(self, port, baudrate):
		"""
		Open a link to a Piksi GPS.
		
		Paramaters
		-----------
		port : string
			Name of port to open.
		baudrate : int
			Port baudrate.
		"""
		try:
			self._driver = PySerialDriver(port, baudrate)
			self._link   = Handler(self._driver.read, self._driver.write, \
							       verbose=self._verbose)
			self.log.info("PORT: %s opened successfully.", port)
		except Exception as e:
			self.log.exception("Failed to open link.")
	
	def close(self, *args):
		"""
		Close the open link if one exists.
		"""
		if self._link is not None:
			try:
				self._link.__exit__(*args)
				self._link=None
				self.log.info("Handler closed successfully.")
			except Exception as e:
				self.log.exception("Failed to close handler.")
		else:
			self.log.error("Cannot close handler as not handler is open.")
		if self._driver is not None:
			try:
				self._driver.__exit__(*args)
				self._driver=None
				self.log.info("PORT:%s closed successfully.")
			except Exception as e:
				self.log.exception("Failed to close PORT:%s.", self._port)
				self.log.critical("PORT:%s failed to close successfully.", self._port)
		else:
			self.log.error("Cannot close port as no port is open.")
			
	def connected(self):
		"""
		Check if a link is open.
		"""
		return self._link is not None
	
	def status(self):
		"""
		Get the current status of the link. [Not implemented]
		"""
		pass
	
	def send_setting(self, grouping, name, value):
		"""
		Send a setting to the GPS module. If self._verbose=True then arguments
		will be validated.
		
		Paramaters
		-----------
		grouping : string
			Grouping name of the setting.
		name : string
			Name of the setting.
		value : string
			Value of the setting as a string.
		"""
		self.log.info("Sending %s.%s=%s to Piksi...", grouping, name, value)
		if self.connected():
			if self._verbose:
				if not piksi_settings.validate(grouping, name, value):
					self.log.error("Arguments were not valid.")
				self.log.debug("Arguments were valid.")
			self._link.send(SBP_MSG_SETTINGS_WRITE, '%s\0%s\0%s\0' % (grouping, name, value))
			time.sleep(0.1)
			self.log.info("Settings sent to Piksi.")
		else:
			self.log.error("Link has not been opened.")
		
	def save_settings(self):
		"""
		Save the current settings to the GPS's flash.
		"""
		self.log.info("Flashing current settings to Piksi...")
		try:
			self._link.send(SBP_MSG_SETTINGS_SAVE, "")
			time.sleep(0.5)
			self._link.send(SBP_MSG_SETTINGS_SAVE, "")
			time.sleep(0.5)
			self._link.send(SBP_MSG_SETTINGS_SAVE, "")
			time.sleep(0.5)
			self._link.send(SBP_MSG_SETTINGS_SAVE, "")
			self.log.info("Completed flashing settings.")
		except Exception as e:
			self.log.exception("Failed to flash settings.")
		
	def read_settings(self):
		"""
		Read the value of the specified setting. [Not implemented]
		"""
		pass
	
	def add_callback(self, callback, SBP_MSG_ID):
		"""
		Add a callback to the read stream.
		
		Paramaters
		-----------
		callback : fn(msg)
			Function which is called whenever specified message is read.
		SBP_MSG_ID : int
			ID of SBP message.
		"""
		self.log.debug("Callback added for SBP_MSG_ID=%d.", SBP_MSG_ID)
		try:
			self._link.add_callback(callback, SBP_MSG_ID)
		except Exception as e:
			self.log.exception("Failed to add callback.")
	
	def start(self):
		"""
		Start the stream reading thread.
		"""
		try:
			self._link.start()
			self.log.info("Started processing SBP messages.")
		except Exception as e:
			self.log.exception("Failed to start processing thread.")
			
	def stop(self):
		"""
		Stop the stream reading thread.
		"""
		try:
			self._link.stop()
			self.log.info("Stopped processing SBP messages.")
		except Exception as e:
			self.log.exception("Failed to stop processing thread.")
			
	def __enter__(self):
		pass
		
	_link    = None
	_driver  = None
	_verbose = None
	_port 	 = None
	log 	 = None
		
