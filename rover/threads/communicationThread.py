import roverMessages as messages
import threading
import socket
import json
from Queue import Queue
import time
from unicodeConvert import convert

class CommunicationThread(threading.Thread):
	def __init__(self, parent, myPort, remotePort):
		threading.Thread.__init__(self)
		self.name = "communicationThread"
		self.parent = parent
		self.debug = False
		self.exit = False
		self.mailbox = Queue()
		self.myPort = myPort
		self.remotePort = remotePort
		self.baseAddress = None
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.setblocking(0)
		self.socket.bind(("", myPort))

	def run(self):
		while not self.exit:
			try:
				inData, address = self.socket.recvfrom(self.remotePort)
				self.baseAddress = address
			except socket.error: # no incoming data
				pass
			else:
				inData = convert(json.loads(inData))
				for key, value in inData.iteritems():
					for msg in messages.cameraList:
						if key == msg:
							self.parent.cameraThread.mailbox.put({key:value})
							if self.debug:
								print("sent " + msg + " to cameraThread")
					for msg in messages.telemetryList:
						if key == msg:
							self.parent.telemetryThread.mailbox.put({key:value})
							if self.debug:
								print("sent " + msg + " to telemetryThread")
					for msg in messages.driveList:
						if key == msg:
							self.parent.driveThread.mailbox.put({key:value})
							if self.debug:
								print("sent " + msg + " to driveThread")
					for msg in messages.armList:
						if key == msg:
							self.parent.armThread.mailbox.put({key:value})
							if self.debug:
								print("sent " + msg + " to armThread")
					for msg in messages.experimentList:
						if key == msg:
							self.parent.experimentThread.mailbox.put({key:value})
							if self.debug:
								print("sent " + msg + " to experimentThread")

			if not self.mailbox.empty():
				outDict = {}
				while not self.mailbox.empty():
					outDict.update(self.mailbox.get())
				outData = json.dumps(outDict)
				if self.baseAddress != None:
					self.socket.sendto(outData, self.baseAddress)
			time.sleep(0.01)


	def stop(self):
		self.exit = True

