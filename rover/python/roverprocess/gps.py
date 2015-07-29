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
                      default=['/dev/ttyUSB1'], nargs=1,
                      help="specify the serial port to use.")
          args = parser.parse_args()

          # Open a connection to Piksi using the default baud rate (1Mbaud)
          self.driver = PySerialDriver(args.port[0], baud=1000000)
          self.handler = Handler(self.driver.read, self.driver.write, verbose=True)
          #self.handler.add_callback(self.pos_callback, msg_type=SBP_MSG_POS_LLH)
          self.handler.start()

	def loop(self):
                # print self.driver.read(4)
                self.getPos()
		time.sleep(1)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "gpsMsg" in message:
			print "got: " + str(message["gpsMsg"])
                        self.getPos()

	def cleanup(self):
                self.handler.stop()
		RoverProcess.cleanup(self)

	# additional functions go here

        # def pos_callback(self, msg):
        #     p = MsgPosLLH(msg)
        #     print "%.4f,%.4f,%.4f,%.i" % \
        #             (p.lat, p.lon, p.height, p.flags)

        def getPos(self):
            #wait for a POS_LLH mesg (1 second timeout)
            p = MsgPosLLH(self.handler.wait(msg_type=SBP_MSG_POS_LLH, timeout=5.0))
            if not p == None:
                print "%.4f,%.4f,%.4f,%.i" % \
                        (p.lat, p.lon, p.height, p.flags)

