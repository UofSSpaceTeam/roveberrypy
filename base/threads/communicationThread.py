import baseMessages as messages
import threading
import socket
import json
from Queue import Queue
import time
from unicodeConvert import convert

class CommunicationThread(threading.Thread):
	def __init__(self, parent, myPort, roverIP, roverPort):
		threading.Thread.__init__(self)
		self.name = "communicationThread"
		self.parent = parent
		self.debug = False
		self.mailbox = Queue()
		self.myPort = myPort
		self.roverIP = roverIP
		self.roverPort = roverPort
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.setblocking(0)
		self.socket.bind(("", myPort))

	def run(self):
		while True:
			try:
				inData, address = self.socket.recvfrom(8192)
			except socket.error: # no incoming data
				pass
			else:
				inData = convert(json.loads(data))
				for key, value in inData.iteritems():
					for msg in messages.inputList:
						if key == msg:
							self.parent.inputThread.mailbox.put({key:value})
							if self.debug:
								print("sent " + msg + " to inputThread")
					for msg in messages.navList:
						if key == msg:
							self.parent.navThread.mailbox.put({key:value})
							if self.debug:
								print("sent " + msg + " to navThread")
					for msg in messages.panelList:
						if key == msg:
							self.parent.panelThread.mailbox.put({key:value})
							if self.debug:
								print("sent " + msg + " to panelThread")
					for msg in messages.guiList:
						if key == msg:
							self.parent.mailbox.put({key:value})
							if self.debug:
								print("sent " + msg + " to guiThread")

			if not self.mailbox.empty():
				outDict = {}
				while not self.mailbox.empty():
					outDict.update(self.mailbox.get())
				outData = json.dumps(outDict)
				print outData
				self.socket.sendto(outData, (self.roverIP, self.roverPort))
			time.sleep(0.01)

