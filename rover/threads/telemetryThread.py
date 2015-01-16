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
		#self.commThread = commThread
		self.mailbox = Queue()

	def run(self):
		while not self.exit:
			print(self.mailbox.get())
			time.sleep(0.01)
			#msg = {}
			# send result from sensor
			# for test just add wanted values  
			#msg["tsense"] = 0.5  
			#self.commThread.mailbox.put(msg)
			#time.sleep(0.2)

	def stop(self):
		self.exit = True