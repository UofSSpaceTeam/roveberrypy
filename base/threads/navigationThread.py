import config.baseMessages
import threading
import json
from Queue import Queue
import time
import unicodeConvert

convert = unicodeConvert.convert

class navigationThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "navigationThread"
		self.exit = False
		self.mailbox = Queue()

	def run(self):
		while not self.exit:
			data = "HELLO FROM NAVTHREAD"
			#print data
			self.mailbox.put(data)
			time.sleep(1)

	def stop(self):
		self.exit = True