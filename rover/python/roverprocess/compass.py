from roverprocess import RoverProcess

import time
import smbus


class Compass(RoverProcess):

	def setup(self, args):
		self.i2c = smbus.SMBus(1)
		self.magAddress = 0x1e
		self.i2cSem = args["sem"]
		self.update = False
                self.i2c.write_byte_data(self.magAddress, 0x02, 0x00) #put in continuous mode

	def loop(self):
                self.i2c.write_byte(self.magAddress, 0x03)
                x = self.i2c.read_byte(self.magAddress) << 8
                x | self.i2c.read_byte(self.magAddress)
                z = self.i2c.read_byte(self.magAddress) << 8
                z | self.i2c.read_byte(self.magAddress)
                y = self.i2c.read_byte(self.magAddress) << 8
                y | self.i2c.read_byte(self.magAddress)

                print "{0}, {1}, {2}".format(x,y,z)

		time.sleep(0.250)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)

	def cleanup(self):
		RoverProcess.cleanup(self)


