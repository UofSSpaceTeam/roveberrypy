import logging, time, sys, itertools
from gps_base import PiksiBaseSatObs
from gps_rover import PiksiRoverSatObs

def main():
    # vars
    BSOB_PORT = 'COM4'
    BSOB_BAUD = 1000000

    RSOI_PORT = 'COM5'
    RSOI_BAUD = 1000000

    UDP_ADDR = '127.0.0.1'
    UDP_PORT = 13320

    ROVER_GPS_PORT = 'COM3'
    ROVER_GPS_BAUD = 1000000

    # logger
    log = logging.getLogger(__name__)
    log.info("Initializing satelite observation bridge")
	
	with PiksiBaseSatObs(BSOB_PORT, BSOB_BAUD, UDP_ADDR, UDP_PORT) as bsob, PiksiRoverSatObs(RSOI_PORT, RSOI_BAUD, UDP_ADDR, UDP_PORT) as rsoi:
		bsob.start()
		rsoi.start()
		log.info("Satelite observation bridge is running")
		try:
			syms = itertools.cycle(['[      ]', '[>     ]', '[=>    ]', '[==>   ]', \
			'[ ==>  ]', '[  ==> ]', '[   ==>]', '[    ==]', '[     =]', '[      ]', \
			'[      ]', '[      ]', '[      ]', '[      ]', '[      ]', '[      ]', \
			'[      ]', '[      ]', '[      ]', '[      ]'])
			sys.stdout.write('    ')
			sys.stdout.flush()
			while True:
				sys.stdout.write(syms.next())
				sys.stdout.flush()
				time.sleep(0.15)
				sys.stdout.write('\b\b\b\b\b\b\b\b')
				sys.stdout.flush()
		except KeyboardInterrupt:
			sys.stdout.write('\b\b\b\b\b\b\b\b\b\b\b\b')
    log.info("Satelite observation bridge has been closed")

if __name__ == "__main__":
    main()
