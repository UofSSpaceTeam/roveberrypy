import baseMessages
import threading
import socket
import json
import pygame
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

class inputThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "inputThread"
		self.commThread = None
		self.exit = False
		self.mailbox = Queue()
		self.cont = [False, False]
		pygame.init()
		if pygame.joystick.get_count() > 0:
			self.cont[0] = pygame.joystick.Joystick(0)
			self.cont[0].init()
		if pygame.joystick.get_count() > 1:
			self.cont[1] = pygame.joystick.Joystick(1)
			self.cont[1].init()

	def run(self):
		while not self.exit:
			msg = {}
			pygame.event.pump()
			if self.cont[0]:
				pass
				# uncomment messages as needed.
				# msg["c1t"] = self.filter(self.cont[0].get_axis(2) * -1)
				# msg["c1j1x"] = self.filter(self.cont[0].get_axis(0))
				# msg["c1j1y"] = self.filter(self.cont[0].get_axis(1) * -1)
				# msg["c1j2x"] = self.filter(self.cont[0].get_axis(4))
				# msg["c1j2y"] = self.filter(self.cont[0].get_axis(3) * -1)
				# msg["c1b_a"] = self.cont[0].get_button(0)
				# msg["c1b_b"] = self.cont[0].get_button(1)
				# msg["c1b_x"] = self.cont[0].get_button(2)
				# msg["c1b_y"] = self.cont[0].get_button(3)
				# msg["c1b_lb"] = self.cont[0].get_button(4)
				# msg["c1b_rb"] = self.cont[0].get_button(5)
				# msg["c1b_ba"] = self.cont[0].get_button(6)
				# msg["c1b_st"] = self.cont[0].get_button(7)
				# msg["c1d_x"] = self.cont[0].get_hat(0)[0]
				# msg["c1d_y"] = self.cont[0].get_hat(0)[1]
			# if self.cont[1]:
				# uncomment messages as needed.
				# msg["c2t"] = self.filter(self.cont[1].get_axis(2) * -1)
				# msg["c2j1x"] = self.filter(self.cont[1].get_axis(0))
				# msg["c2j1y"] = self.filter(self.cont[1].get_axis(1) * -1)
				# msg["c2j2x"] = self.filter(self.cont[1].get_axis(4))
				# msg["c2j2y"] = self.filter(self.cont[1].get_axis(3) * -1)
				# msg["c2b_a"] = self.cont[1].get_button(0)
				# msg["c2b_b"] = self.cont[1].get_button(1)
				# msg["c2b_x"] = self.cont[1].get_button(2)
				# msg["c2b_y"] = self.cont[1].get_button(3)
				# msg["c2b_lb"] = self.cont[1].get_button(4)
				# msg["c2b_rb"] = self.cont[1].get_button(5)
				# msg["c2b_ba"] = self.cont[1].get_button(6)
				# msg["c2b_st"] = self.cont[1].get_button(7)
				# msg["c2d_x"] = self.cont[1].get_hat(0)[0]
				# msg["c2d_y"] = self.cont[1].get_hat(0)[1]	
			if self.cont[0] or self.cont[1]:
				self.commThread.mailbox.put(msg)
			time.sleep(0.2)

	def stop(self):
		self.exit = True
	
	def filter(self, value):
		if abs(value) < 0.15:
			return 0.0
		elif value > 1.0:
			return 1.0
		elif value < -1.0:
			return -1.0
		return value

class navigationThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "navigationThread"
		self.exit = False
		self.mailbox = Queue()

	def run(self):
		while not self.exit:
			time.sleep(0.01)

	def stop(self):
		self.exit = True

class panelThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "panelThread"
		self.exit = False
		self.mailbox = Queue()

	def run(self):
		while not self.exit:
			time.sleep(0.01)

	def stop(self):
		self.exit = True

class guiThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "guiThread"
		self.exit = False
		self.mailbox = Queue()

	def run(self):
		while not self.exit:
			time.sleep(0.01)

	def stop(self):
		self.exit = True

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
				self.parentThread.inbox.put(data)

		def stop(self):
			self.exit = True


	def __init__(self):
		threading.Thread.__init__(self)
		self.debug = True
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
					for msg in roverMessages.inputList:
						if key == msg:
							self.inputThread.mailbox.put({key, value})
							if self.debug:
								print("sent " + msg + " to inputThread")
					for msg in roverMessages.navList:
						if key == msg:
							self.navThread.mailbox.put({key, value})
							if self.debug:
								print("sent " + msg + " to navThread")
					for msg in roverMessages.panelList:
						if key == msg:
							self.panelThread.mailbox.put({key, value})
							if self.debug:
								print("sent " + msg + " to panelThread")
					for msg in roverMessages.guiList:
						if key == msg:
							self.guiThread.mailbox.put({key, value})
							if self.debug:
								print("sent " + msg + " to guiThread")
				
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
