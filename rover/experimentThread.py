import roverMessages
import threading
import json
from Queue import Queue
import time

class experimentThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "experimentThread"
		self.exit = False
		self.mailbox = Queue()

	def run(self):
		while not self.exit:
			time.sleep(0.01)

	def stop(self):
		self.exit = True