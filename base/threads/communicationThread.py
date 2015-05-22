import baseMessages as messages
import threading
import socket
import json
from Queue import Queue
import time
from unicodeConvert import convert

class CommunicationThread(threading.Thread):
	def __init__(self, parent, roverIP, towerIP, port):
		threading.Thread.__init__(self)
		self.parent = parent
		self.period = 0.05
		self.mailbox = Queue()
		self.port = port
		self.roverIP = roverIP
		self.towerIP = towerIP
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.setblocking(0)
		self.socket.bind(("", port))

	def run(self):
		while True:
			try:
				inData, address = self.socket.recvfrom(self.port)
				#print(inData)
			except socket.error: # no incoming data
				pass
			else:
				inData = convert(json.loads(inData))
				for key, value in inData.iteritems():
					for msg in messages.inputList:
						if key == msg:
							self.parent.inputThread.mailbox.put({key:value})
					for msg in messages.navList:
						if key == msg:
							self.parent.navThread.mailbox.put({key:value})
					for msg in messages.guiList:
						if key == msg:
							self.parent.mailbox.put({key:value})
					for msg in messages.telemetryList:
						if key == msg:
							self.parent.teleThread.mailbox.put({key:value})

			if not self.mailbox.empty():
				outDict = {}
				while not self.mailbox.empty():
					outDict.update(self.mailbox.get())
				outData = json.dumps(outDict)
				print outData
				self.socket.sendto(outData, (self.roverIP, self.port))
				self.socket.sendto(outData, (self.towerIP, self.port))
			time.sleep(0.05)

