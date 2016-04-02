from RoverProcess import RoverProcess

from libusst.external.sbp.client.drivers.pyserial_driver import PySerialDriver
from libusst.external.sbp.client.handler import Handler
from libusst.nav.gps_logger import GPSLogger

import time
import logging

class GPSProcess(object):
	freq = 10
	port = 'COM5'
	baud = 1000000
	
	_link 	= None
	_driver = None
	log 	= None
	
	gps_logger = None
	
	def setup(self, args):
		self.log = logging.getLogger(__name__)
		self.log.info("Initializing...")
		self.getArgs(args)
		self.open(self.port, self.baud)
		self.log.info("Connection opened on '%s'", self.port)
		logfile = time.strftime("C:\scratch\sbp-%Y%m%d-%H%M%S.log")
		self.gps_logger = GPSLogger(logfile)
		self._link.add_callback(self.gps_logger)
		self.log.info("Setup complete")
		self._link.start()
	
	def loop(self):
		llh = self.gps_logger.getLast(0x201)
		ned = self.gps_logger.getLast(0x203)
		self.setShared("lattitude", llh.lat)
		self.setShared("longitude", llh.lon)
		self.setShared("tow", 		llh.tow)
		self.setShared("altitude", 	llh.height)
		self.setShared("n_sats", 	llh.n_sats)
		self.setShared("llh_flags", llh.flags)
		self.setShared("baseline_n", ned.n)
		self.setShared("baseline_e", ned.e)
		self.setShared("baseline_d", ned.d)
		self.setShared("baseline_flags", ned.flags)
		time.sleep(1/self.freq)
	
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
	
	def cleanup(self):
		RoverProcess.cleanup(self)
		self.log.info("Closing connections...")
		self._link.__exit__()
		self._driver.__exit__()
		self.log.info("Closed succefully")
		
	def getArgs(self, args):
		if 'port' in args.keys():
			self.port = args['port']
		if 'baud' in args.keys():
			self.baud = args['baud']
		if 'freq' in args.keys():
			self.freq = args['freq']	
			
	def open(self, port, baudrate):
		opened = False
		try:
			self._driver = PySerialDriver(port, baudrate)
			opened = True
		except (SystemExit, Exception) as e:
			self.log.exception("Unabled to open \'%s\'. Attempting to open connection...", port)
			time.sleep(0.1)
		while not opened:
			try:
				self._driver = PySerialDriver(port, baudrate)
				opened = True
			except (SystemExit, Exception) as e:
				self.log.error("Attempt to open '%s' failed. Retrying...", port)
				time.sleep(0.1)
		opened = False
		while not opened:
			try:
				self._link = Handler(self._driver.read, self._driver.write)
				opened = True
			except (SystemExit, Exception) as e:
				self.log.error("Attempt to open Handler failed. Retrying...")
				time.sleep(0.1)
				

