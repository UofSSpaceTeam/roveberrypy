import roverMessages
import threading
import json
from Queue import Queue
import time
import unicodeConvert

convert = unicodeConvert.convert

class driveThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "driveThread"
		self.exit = False
		self.mailbox = Queue()

	def run(self):
		while not self.exit:
			data = str(self.mailbox.get())
			print data
			time.sleep(0.01)

	def stop(self):
		self.exit = True