from roverprocess import RoverProcess
from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client.handler import Handler
from sbp.navigation import SBP_MSG_POS_LLH, MsgPosLLH
from sbp.system import SBP_MSG_HEARTBEAT, MsgHeartbeat
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
          self.driver = PySerialDriver(args.port[0], baud=1000000)
          self.handler = Handler(self.driver.read, self.driver.write, verbose=True)
          self.handler.add_callback(self.posLLH_callback, msg_type=SBP_MSG_POS_LLH)
          self.handler.start()

	def loop(self):
                # print self.driver.read(4)
		time.sleep(1)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "gpsMsg" in message:
			print "got: " + str(message["gpsMsg"])

	def cleanup(self):
		RoverProcess.cleanup(self)
                self.handler.stop()

	# additional functions go here

        def posLLH_callback(self, msg):
            # This is called every time we receive a POS_LLH message
            p = MsgPosLLH(msg)

            # Print out the latitude, longtitude, and height
            print "%.4f,%.4f,%.4f" % \
                    (p.lat, p.lon, p.height)


