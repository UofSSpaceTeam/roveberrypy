from roverprocess import RoverProcess
from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client.handler import Handler
from sbp.navigation import SBP_MSG_POS_LLH, MsgPosLLH
import time

class GPS(RoverProcess):

	# helper classes go here if you want any

	def setup(self, args):
          import argparse
          parser = argparse.ArgumentParser(description="Swift Navigation SBP Example.")
          parser.add_argument("-p", "--port",
                      default=['/dev/ttyUSB0'], nargs=1,
                      help="specify the serial port to use.")
          args = parser.parse_args()

          # Open a connection to Piksi using the default baud rate (1Mbaud)
          driver = PySerialDriver(args.port[0], baud=1000000)
          handler = Handler(driver.read, driver,write, verbose=True)
          handler.add_callback(posLLH_callback, msg_type=SBP_MSG_POS_LLH)

	def loop(self):
		time.sleep(1)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "gpsMsg" in message:
			print "got: " + str(message["gpsMsg"])

	def cleanup(self):
		RoverProcess.cleanup(self)



	# additional functions go here

        def posLLH_callback(msg):
            # This is called every time we receive a POS_LLH message
            p = MsgPosLLH(msg)

            # Print out the latitude, longtitude, and height
            print "%.4f,%.4f,%.4f" % \
                    (p.lat, p.lon, p.height)


