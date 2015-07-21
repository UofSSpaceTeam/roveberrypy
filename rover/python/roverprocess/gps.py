from roverprocess import RoverProcess
from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client.handler import Handler
from sbp.navigation import SBP_MSG_BASELINE_NED, MsgBaselineNED

# your imports go here. For example:
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
          handler.add_callback(baseline_callback, msg_type=SBP_MSG_BASELINE_NED)

	def loop(self):
		time.sleep(1)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "gpsMsg" in message:
			print "got: " + str(message["gpsMsg"])

	def cleanup(self):
		RoverProcess.cleanup(self)



	# additional functions go here
        def baseline_callback(msg):
          # This function is called every time we receive a BASELINE_NED message

          # First decode the SBP message in "msg" into a python object, the sbp library
          # has functions that do this for all the message types defined in the
          # specification.
          b = MsgBaselineNED(msg)

          # b now contains the decoded baseline information and
          # has fields with the same names as in the SBP docs

          # Print out the N, E, D coordinates of the baseline
          print "%.4f,%.4f,%.4f" % \
            (b.n * 1e-3, b.e * 1e-3, b.d * 1e-3)


