import roverMessages
import threading
import json
from Queue import Queue
import time
from unicodeConvert import convert

class armThread(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "armThread"
		self.exit = False
		self.mailbox = Queue()

	def run(self):
		while not self.exit:
			time.sleep(0.01)

	def stop(self):
		self.exit = True