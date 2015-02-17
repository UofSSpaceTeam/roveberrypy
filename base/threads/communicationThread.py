import config.baseMessages as messages
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
			self.debug = True
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
					self.socket.sendto(data, ("192.168.1.2", self.port))
					if self.debug:
						print("broadcast: " + data)
				time.sleep(0.01)

		def stop(self):
			self.exit = True

	class receiveThread(threading.Thread):
		def __init__(self):
			threading.Thread.__init__(self)
			self.debug = True
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
		self.sendInterval = None
		self.sendPort = None
		self.receivePort = None
		self.inputThread = None
		self.navThread = None
		self.panelThread = None
		self.guiThread = None

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
				for key, value in inData.iteritems():
					for msg in messages.inputList:
						if key == msg:
							self.inputThread.mailbox.put({key, value})
							if self.debug:
								print("sent " + msg + " to inputThread")
					for msg in messages.navList:
						if key == msg:
							self.navThread.mailbox.put({key, value})
							if self.debug:
								print("sent " + msg + " to navThread")
					for msg in messages.panelList:
						if key == msg:
							self.panelThread.mailbox.put({key, value})
							if self.debug:
								print("sent " + msg + " to panelThread")
					for msg in messages.guiList:
						if key == msg:
							self.guiThread.mailbox.put({key, value})
							if self.debug:
								print("sent " + msg + " to guiThread")
				
			# process output from other threads
			outDict = {}
			if not self.mailbox.empty():
				while not self.mailbox.empty():
					outDict.update(self.mailbox.get())
				if(self.debug):
					print "sending: " + str(outDict)
				self.sender.mailbox.put(outDict)
				self.guiThread.mailbox.put(outDict)
			time.sleep(0.01)

	def stop(self):
		self.sender.stop()
		self.receiver.stop()
		self.exit = True
