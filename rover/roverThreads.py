import threading
import socket
import json
from Queue import Queue
import time

# recursive function I stole to strip unicode from dictionaries
def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

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
			self.socket.bind(("", self.port))
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
			while not self.exit:
				while not self.mailbox.empty():
					data = json.dumps(self.mailbox.get())
					self.socket.sendto(data, ("<broadcast>", 8000))
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
				self.parentThread.inbox.put(data)

		def stop(self):
			self.exit = True


	def __init__(self):
		threading.Thread.__init__(self)
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

	def run(self):
		self.sender.port = self.sendPort
		self.receiver.port = self.receivePort
		self.sender.start()
		self.receiver.start()
		lastSend = time.clock()
		while not self.exit:
			# process network input
			while not self.inbox.empty():
				inData = self.inbox.get()
				# todo: parse and distribute items according to some lists
			# process output from other threads
			if time.clock() - lastSend > self.sendInterval:
				lastSend = time.clock()
				outDict = {}
				while not self.mailbox.empty():
					outDict.update(self.mailbox.get())
				self.sender.mailbox.put(outDict)
			time.sleep(0.01)

	def stop(self):
		self.sender.stop()
		self.receiver.stop()
		self.exit = True

class cameraThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "cameraThread"
		self.exit = False
		self.mailbox = Queue()

	def run(self):
		while not self.exit:
			time.sleep(0.01)

	def stop(self):
		self.exit = True

class telemetryThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "telemetryThread"
		self.exit = False
		self.mailbox = Queue()

	def run(self):
		while not self.exit:
			time.sleep(0.01)

	def stop(self):
		self.exit = True

class driveThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "driveThread"
		self.exit = False
		self.mailbox = Queue()

	def run(self):
		while not self.exit:
			time.sleep(0.01)

	def stop(self):
		self.exit = True

class armThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "armThread"
		self.exit = False
		self.mailbox = Queue()

	def run(self):
		while not self.exit:
			time.sleep(0.01)

	def stop(self):
		self.exit = True

class experimentThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "experimentThread"
		self.exit = False
		self.mailbox = Queue()

	def run(self):
		while not self.exit:
			time.sleep(0.01)

	def stop(self):
		self.exit = True

