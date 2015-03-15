import baseMessages as messages
import threading
from Queue import Queue
import time
import unicodeConvert

convert = unicodeConvert.convert

class PanelThread(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.name = "panelThread"
		self.parent = parent
		self.mailbox = Queue()

	def run(self):
		while True:
			time.sleep(0.01)

