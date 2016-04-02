from sbp.client import Handler, Framer
from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client.handler import Handler
from sbp.client.loggers.udp_logger import UdpLogger
from sbp.observation import SBP_MSG_OBS, SBP_MSG_BASE_POS_ECEF, SBP_MSG_BASE_POS_LLH

import socket
import time

OBS_MSGS = [SBP_MSG_OBS, SBP_MSG_BASE_POS_ECEF, SBP_MSG_BASE_POS_LLH]

class PiksiBaseSatObs(object):
	def __init__(self, serport, serbaud, udpaddr, udpport):
		self._serport = serport
		self._serbaud = serbaud
		self._udpaddr = udpaddr
		self._udpport = udpport
		self._satobs_thread = threading.Thread(target=self._satobs_bridge)
		self._satobs_thread.daemon = True
		
	def __enter__(self):
		self.start()
	
	def __exit__(self):
		self.stop()
	
	def start(self):
		self._running = True
		self._satobs_thread.start()
	
	def stop(self):
		self._running = False
		self._satobs_thread.join(1)
		
	def _satobs_bridge(self):
		with PySerialDriver(self._serport, self._serbaud) as ser:
			with Handler(Framer(ser.read, ser.write)) as link:
				with UdpLogger(self._udpaddr, self._udpport) as udp:
					link.add_callback(udp, OBS_MSGS)
					while self._running:
						time.sleep(0.1)
					
	def is_alive(self):
		return self._satobs_thread.is_alive()
			
	_serport = None
	_serbaud = None
	_udpaddr = None
	_udpport = None
	_running = False
	_satobs_thread = None	