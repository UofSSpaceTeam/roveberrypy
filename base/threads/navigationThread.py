import baseMessages as messages
import threading
import json
from Queue import Queue
import time
import unicodeConvert

convert = unicodeConvert.convert

class NavigationThread(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.name = "navigationThread"
		self.parent = parent
		self.mailbox = Queue()

	def run(self):
		while True:
			data = "HELLO FROM NAVTHREAD"
			#print data
			#self.mailbox.put(data)
			time.sleep(1)

