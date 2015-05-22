import roverMessages as messages
import threading
import socket
import json
from Queue import Queue
import time
from unicodeConvert import convert

class CommunicationThread(threading.Thread):
	def __init__(self, parent, port):
		threading.Thread.__init__(self)
		self.period = 0.05
		self.parent = parent
		self.name = "Communication"
		self.mailbox = Queue()
		self.port = port
		self.baseAddress = None
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.setblocking(0)
		self.socket.bind(("", port))

	def run(self):
		while True:
			time.sleep(self.period)
			try:
				inData, address = self.socket.recvfrom(8192)
				self.baseAddress = address
			except socket.error: # no data
				continue
			else:
				inData = convert(json.loads(inData))
				for key, value in inData.iteritems():
					for msg in messages.cameraList:
						if key == msg:
							self.parent.cameraThread.mailbox.put({key:value})
					for msg in messages.telemetryList:
						if key == msg:
							self.parent.telemetryThread.mailbox.put({key:value})
					for msg in messages.driveList:
						if key == msg:
							self.parent.driveThread.mailbox.put({key:value})
					for msg in messages.armList:
						if key == msg:
							self.parent.armThread.mailbox.put({key:value})
					for msg in messages.experimentList:
						if key == msg:
							self.parent.experimentThread.mailbox.put({key:value})

				outDict = {}
				while not self.mailbox.empty():
					outDict.update(self.mailbox.get())
				outData = json.dumps(outDict)
				if self.baseAddress is not None:
					self.socket.sendto(outData, self.baseAddress)

