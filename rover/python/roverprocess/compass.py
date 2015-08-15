from roverprocess import RoverProcess

import time
import serial


class Compass(RoverProcess):

	def setup(self, args):
		self.serial = serial.Serial(port="/dev/ttyAMA0", baudrate=9600, timeout=1)
		self.update = False
<<<<<<< HEAD


	def loop(self):
		# inchar = self.serial.read(1)
		# if(inchar == "$"):
			# data = self.serial.readline()
			# print "read complete", data
		# else:
			# print "no data, got: ", inchar
			
		print self.serial.read(1)
		
		time.sleep(0.01)
		

=======
            self.serial = open('/dev/ttyACM1', 'r+')


	def loop(self):
            self.serial.write('r')
            print(self.serial.read())
		time.sleep(0.250)
>>>>>>> origin/master

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)

	def cleanup(self):
		RoverProcess.cleanup(self)


