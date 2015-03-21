# a tread to test sending sensor data
# based on the code in inputThread.py

import roverMessages
import threading
import json
from Queue import Queue
import time
from unicodeConvert import convert

class sensorTestTread((threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "sensorThread"
		self.commThread = None
		self.exit = False
		self.mailbox = Queue()
		
		
	def run(self):
		while not self.exit:
			msg = {}
			# send result from sensor
			# for test just add wanted values  
			msg["tsense"] = 0.5  
			self.commThread.mailbox.put(msg)
			time.sleep(0.2)
			
	def stop(self):
		self.exit = True