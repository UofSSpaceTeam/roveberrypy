from roverprocess import RoverProcess

import time


class Compass(RoverProcess):

	def setup(self, args):
		self.update = False
                self.serial = open('/dev/ttyACM1', 'r+')


	def loop(self):
                self.serial.write('r')
                print(self.serial.read())
		time.sleep(0.250)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)

	def cleanup(self):
		RoverProcess.cleanup(self)


