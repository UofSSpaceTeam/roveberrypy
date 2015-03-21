import roverMessages as messages
import threading
import socket
import json
from Queue import Queue
import time
import unicodeConvert

convert = unicodeConvert.convert

class communicationThread(threading.Thread):

	class sendThread(threading.Thread):
		def __init__(self):
			threading.Thread.__init__(self)
			self.debug = False
			self.name = "sendThread"
			self.exit = False
			self.mailbox = Queue()
			self.socket = None
			self.port = None

		def run(self):
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
			self.socket.bind(("", self.port))
			while not self.exit:
				while not self.mailbox.empty():
					data = json.dumps(self.mailbox.get())
					self.socket.sendto(data, ("<broadcast>", self.port))
					if self.debug:
						print("broadcast: " + data)
				time.sleep(0.01)

		def stop(self):
			self.exit = True

	class receiveThread(threading.Thread):
		def __init__(self):
			threading.Thread.__init__(self)
			self.debug = False
			self.name = "receiveThread"
			self.exit = False
			self.parentThread = None

		def run(self):
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.socket.bind(("", self.port))
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
			self.socket.settimeout(0.25)
			while not self.exit:
				try:
					data, address = self.socket.recvfrom(8192)
				except socket.timeout:
					continue
				if self.debug:
					print("received: " + data + " from " + str(address))
				data = convert(json.loads(data))
				#print data
				self.parentThread.inbox.put(data)

		def stop(self):
			self.exit = True


	def __init__(self):
		threading.Thread.__init__(self)
		self.debug = False
		self.name = "communicationThread"
		self.exit = False
		self.mailbox = Queue()
		self.inbox = Queue()
		self.sender = self.sendThread()
		self.receiver = self.receiveThread()
		self.receiver.parentThread = self
		self.sendPort = None
		self.receivePort = None
		self.cameraThread = None
		self.teleThread = None
		self.driveThread = None
		self.armThread = None
		self.experimentThread = None

	def run(self):
		self.sender.port = self.sendPort
		self.receiver.port = self.receivePort
		self.sender.start()
		self.receiver.start()
		lastSend = time.clock()
		while not self.exit:
			# process and distribute input from network
			while not self.inbox.empty():
				inData = self.inbox.get()
				#print inData
				for key, value in inData.iteritems():
					for msg in messages.cameraList:
						if key == msg:
							self.cameraThread.mailbox.put({key:value})
							if self.debug:
								print("delivered " + msg + " to cameraThread")
					for msg in messages.telemetryList:
						if key == msg:
							self.teleThread.mailbox.put({key:value})
							if self.debug:
								print("delivered " + msg + " to telemetryThread")
					for msg in messages.driveList:
						if key == msg:
							self.driveThread.mailbox.put({key:value})
							if self.debug:
								print("delivered " + msg + " to driveThread")
					for msg in messages.armList:
						if key == msg:
							self.armThread.mailbox.put({key:value})
							if self.debug:
								print("delivered " + msg + " to armThread")
					for msg in messages.experimentList:
						if key == msg:
							self.experimentThread.mailbox.put({key:value})
							if self.debug:
								print("delivered " + msg + " to experimentThread")
				
			# process output from other threads
			outDict = {}
			if not self.mailbox.empty():
				while not self.mailbox.empty():
					outDict.update(self.mailbox.get())
				if(self.debug):
					print "sending: " + str(outDict)
				self.sender.mailbox.put(outDict)
			time.sleep(0.01)

	def stop(self):
		self.sender.stop()
		self.receiver.stop()
		self.exit = True
