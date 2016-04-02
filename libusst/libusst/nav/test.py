
from libusst.external.sbp.client.drivers.pyserial_driver 	import PySerialDriver
from libusst.external.sbp.client.handler            		import Handler
from libusst.nav.gps_logger 		import GPSLogger

import struct
import time
import logging

DEFAULT_LOG_FILENAME = time.strftime("C:\scratch\sbp-%Y%m%d-%H%M%S.log")

gpsl=None

def run():
	global gpsl
	log = logging.getLogger(__name__)
	logging.basicConfig(filename="C:\scratch\sys_log.log", level=logging.DEBUG)
	log.info("Connecting to COM5...")
	with PySerialDriver('com4', 1000000) as driver:
		log.info("Connection successful.")
		log.info("Opening SBP handler...")
		with Handler(driver.read, driver.write) as handler:
			log.info("SBP handler connected.")
			log.info("Opening JSON logger...")
			log.info("Beginning writing...")
			log.info("Writing...")
			json = GPSLogger(DEFAULT_LOG_FILENAME)
			handler.add_callback(json)
			gpsl=json
			try:
				while True:
					time.sleep(0.1)
			except KeyboardInterrupt:
				print json.recent[0x201]
				print json.recent[0x203]
				return



