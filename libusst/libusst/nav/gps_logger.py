from libusst.external.sbp.client.drivers.pyserial_driver 	import PySerialDriver
from libusst.external.sbp.client.handler            		import Handler
from libusst.external.sbp.client.loggers.base_logger 		import BaseLogger
import json
import time
import logging
import collections

class GPSLogger(BaseLogger):
	def __init__(self, filename, *args):
		# Setup Logger.
		BaseLogger.__init__(self, filename)
		self.sys_log = logging.getLogger(__name__)
		self._record_ids = args
		self.rbuf = dict()
		# Build rbuf and write log information.
		log_info = "Recording SBP_MSG_ID's: "
		for sbp_msg_id in args:
			self.rbuf[sbp_msg_id] = []
			log_info += sbp_msg_id.__str__() + ", "
		log_info = log_info[:-2]
		self.sys_log.info("Logger created, directed to: \"%s\"", filename)
		self.sys_log.info(log_info)
		
	def __call__(self, msg):
		self.call(msg)
	
	def fmt_msg(self, msg):
		# Parse message.
		dispatched_msg = self.dispatch(msg)
		# If it is a message we are directed to record then record it.
		if msg.msg_type in self._record_ids:
			self.rbuf[msg.msg_type].append(dispatched_msg)
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
	
	_record_ids	= None
	rbuf		= None
	sys_log		= None
		