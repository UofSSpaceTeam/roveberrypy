import roverMessages
import threading
import json
from Queue import Queue
import time
import unicodeConvert

convert = unicodeConvert.convert

class telemetryThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "telemetryThread"
		self.exit = False
		self.commThread = None
		self.mailbox = Queue()

		
	def run(self):
		while not self.exit:
			msg = {}
			# get info from sensor every 1 sec
			time.sleep(1)
			msg.update(self.sensorInfo())
			#data = json.dumps(msg)
			self.commThread.mailbox.put(msg)
			self.mailbox.put(msg)
			time.sleep(.2)
			
	# simulates receiving info from a sensor  		
	def sensorInfo(self):
		value = {}
		#add values to test
		#using c1j1y arbitrarily 
		value["c1j1y"] = 0.5
		
		return value 
		

	def stop(self):
		self.exit = True