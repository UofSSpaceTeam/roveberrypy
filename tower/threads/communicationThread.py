import towerMessages as messages
import threading
import socket
import json
from Queue import Queue
import time
from unicodeConvert import convert

class CommunicationThread(threading.Thread):
	def __init__(self, parent, port):
		threading.Thread.__init__(self)
		self.name = "communicationThread"
		self.parent = parent
		self.mailbox = Queue()
		self.port = port
		self.baseAddress = None
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.setblocking(0)
		self.socket.bind(("", port))

	def run(self):
		while True:
			try:
				inData, address = self.socket.recvfrom(self.port)
				self.baseAddress = address
			except socket.error: # no incoming data
				pass
			else:
				inData = convert(json.loads(inData))
				for key, value in inData.iteritems():
					for msg in messages.telemetryList:
						if key == msg:
							self.parent.telemetryThread.mailbox.put({key:value})
					for msg in messages.motorList:
						if key == msg:
							self.parent.motorThread.mailbox.put({key:value})

			if not self.mailbox.empty():
				outDict = {}
				while not self.mailbox.empty():
					outDict.update(self.mailbox.get())
				print outDict
				outData = json.dumps(outDict)
				if self.baseAddress != None:
					self.socket.sendto(outData, self.baseAddress)
			time.sleep(0.1)

