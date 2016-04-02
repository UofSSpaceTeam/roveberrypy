from libusst.external.sbp.client.drivers.pyserial_driver 	import PySerialDriver
from libusst.external.sbp.client.handler            		import Handler
from libusst.external.sbp.client.loggers.base_logger 		import BaseLogger
import json
import time
import logging
import threading

class GPSLogger(BaseLogger):
	def __init__(self, filename):
		# Setup Logger.
		BaseLogger.__init__(self, filename)
		self.sys_log = logging.getLogger(__name__)
		self.recent = dict()
		self.sys_log.info("GPSLogger created, directed to: \"%s\"", filename)
		
	def __call__(self, msg):
		self.call(msg)
	
	def fmt_msg(self, msg):
		# Parse message.
		dispatched_msg = self.dispatch(msg)
		# Update most recent message of type msg.msg_type.
		self.recent[msg.msg_type] = dispatched_msg
		# Add it to the JSON log.
		data = dispatched_msg.to_json_dict()
		return {"delta": self.delta(),
				"timestamp": self.timestamp(),
				"data": data,
				"metadata": self.tags}
				
	def call(self, msg):
		try:
			self.handle.write(json.dumps(self.fmt_msg(msg), allow_nan=False) + "\n")
		except ValueError:
			if self.sys_log is not None:
				self.sys_log.warning("Bad values in JSON encoding for msg_type %d for msg %s"% (msg.msg_type, msg))

	def getLast(self, SBP_MSG_ID):
		return self.recent[SBP_MSG_ID]
		
	recent		= None
	sys_log		= None
		