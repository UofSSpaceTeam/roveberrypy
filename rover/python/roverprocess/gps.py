from roverprocess import RoverProcess
from libs.sbp.pyserial_driver import PySerialDriver
from libs.sbp.handler import Handler
from libs.sbp.navigation import SBP_MSG_POS_LLH, MsgPosLLH
from libs.sbp.navigation import SBP_MSG_BASELINE_NED, MsgBaselineNED
from libs.sbp.settings import SBP_MSG_SETTINGS_WRITE, MsgSettingsWrite
import time

class GPS(RoverProcess):
        '''GPS rover process
        contains a SBP handler for recieving and parsing sbp messages.
        Incomming messages:
            gps_posReq - request the current gps location
            gps_baselineReq - request the relative baseline position
        Outgoing messages:
            gps_Location - the current gps location
            gps_Baseline - the relative base position in NED coordinates.
        '''

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
          #self.handler.add_callback(self.pos_callback, msg_type=SBP_MSG_POS_LLH)
          # self.handler.add_callback(self.baseline_callback, msg_type=SBP_MSG_BASELINE_NED)
          self.handler.start()

	def loop(self):
                self.getPos()
		time.sleep(1)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
                #TODO: more descriptive error handling
		if "gps_PosReq" in message:
                    try:
                        self.getPos()
                    except:
                        print "Error getting position"
                elif "gps_BaselineReq" in message:
                    try:
                        # self.getBaseline()
                        pass
                    except:
                        print "Error getting baseline"

	def cleanup(self):
                try:
                    self.handler.stop()
                except:
                    pass
		RoverProcess.cleanup(self)

	# additional functions go here
        def getPos(self, timeout=5.0):
            ''' Get current gps location
            Unfortunately this crashes if no message is recieved,
            so timeout must be long enough to prevent this.

            SBP_MSG_POS_LLH object is sent under the key "gps_Location"
            '''
            p = MsgPosLLH(self.handler.wait(msg_type=SBP_MSG_POS_LLH, timeout=timeout))
            if not p == None:
                # print "%.6f,%.6f,%.6f,%i" % (p.lat, p.lon, p.height, p.flags)
                self.setShared("gps_Location", p)
                return p

        def getBaseline(self, timeout=5.0):
            ''' Get relative baseline position in NED coordinates
            Same timeout issues as getPos.

            SBP_MSG_BASELINE_NED object is sent under the key "gps_Baseline"
            '''
            b = MsgBaselineNED(self.handler.wait(msg_type=SBP_MSG_BASELINE_NED, timeout=timeout))
            if not b == None:
                # print "%.4f, %.4f, %.4f, %i" % (b.n, b.e, b.d, b.flags)
                self.setShared("gps_Baseline", b)
                return b

        def setBaseLocation(self, p):
            ''' Set the location of a surveyed base location
            p is an SBP_MSG_POS_LLH message containing the gps location of the base station
            '''
            self.handler.send_msg(MsgSettingsWrite(setting="[surveyed position, surveyed alt, {}]".format(p.height)))
            self.handler.send_msg(MsgSettingsWrite(setting="[surveyed position, surveyed lat, {}]".format(p.lat)))
            self.handler.send_msg(MsgSettingsWrite(setting="[surveyed position, surveyed lon, {}]".format(p.lon)))

        # def pos_callback(self, msg):
        #     p = MsgPosLLH(msg)
        #     print "%.4f,%.4f,%.4f,%.i" % \
        #             (p.lat, p.lon, p.height, p.flags)
        #
        # def baseline_callback(self, msg):
        #     b = MsgBaselineNED(msg)
        #     print "%.6f, %.6f, %.6f" % (b.x, b.y, b.z)

