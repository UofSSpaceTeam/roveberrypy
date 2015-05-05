import roverMessages
import threading
import json
from Queue import Queue
import time
#from unicodeConvert import convert
from ServoDriver import *


class antenaCameraThread(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "antenaCameraThread"
		self.exit = False
		self.mailbox = Queue()

	def run(self):
		print "antena thread started"
		servoDriver = ServoDriver()
		pitch = 0
		base = 0
		while True:
			while not self.mailbox.empty():
				data = self.mailbox.get()
				if "c1d_y" in data:
					pitch += int(data["c1d_y"]) * 5
					if pitch > 45:
						pitch = 45
					elif pitch < -45:
						pitch = -45
					#print pitch
				elif "c1d_x" in data:
					base += int(data["c1d_x"]) * 10
					if base > 360:
						base = 360;
					elif base < 0:
						base = 0
					#print base

			if pitch is not None and base is not None:
				if -45 < pitch <= 45:
					pos1 = 28*pitch/3 + 1690
					try:
						servoDriver.setServo(0,int(pos1))
					except:
						print("NaN!")
				if 0 <= base <= 360:
					pos2 = 115*base/36 + 950
					try:
						servoDriver.setServo(1,int(pos2))
					except:
						print("NaN!")
			
			time.sleep(0.01)

	

	def stop(self):
		self._Thread__stop()
