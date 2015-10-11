from roverprocess import RoverProcess

import time
from threading import Thread
from multiprocessing import BoundedSemaphore
import json
import socket

class JsonServer(RoverProcess):

	class ListenThread(Thread):
		def __init__(self, listener, uplink, parent):
			Thread.__init__(self)
			self.listener = listener
			self.uplink = uplink
			self.parent = parent
		
		def run(self):
			while True:
				jsonData, address = self.listener.recvfrom(4096)
				print jsonData
				data = self.byteify(json.loads(jsonData))
				if isinstance(data, dict):
					self.uplink.put(data)
					if "commsHeartbeat" in data:
						self.setShared("commsHeartbeat", True)
					with self.parent.addressSem:
						self.parent.address = address[0]
		
		# Thanks, Mark Amery of stackoverflow!
		def byteify(self, input):
			if isinstance(input, dict):
				return(
						{self.byteify(key): self.byteify(value)
						for key, value in input.iteritems()})
			elif isinstance(input, list):
				return [self.byteify(element) for element in input]
			elif isinstance(input, unicode):
				return input.encode('utf-8')
			else:
				return input
	
	def setup(self, args):
		self.localPort = args["local"]
		self.remotePort = args["remote"]
		self.sendPeriod = args["sendPeriod"]
		self.address = "192.168.1.110"
		self.addressSem = BoundedSemaphore()
		self.data = {}
		self.dataSem = BoundedSemaphore()
		self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.listener.bind(("", self.localPort))
		self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		receiver = JsonServer.ListenThread(self.listener, self.uplink, self)
		receiver.daemon = True
		receiver.start()
		self.load = False
		
	
	def loop(self):
		if self.data:
			with self.dataSem:
				jsonData = json.dumps(self.data)
				self.data = {}
			with self.addressSem:
				if self.address:
					self.sender.sendto(
						jsonData, (self.address, self.remotePort))
		time.sleep(self.sendPeriod)
	
	def messageTrigger(self, message):
		# Prevent threads from triggering before server has started
		while self.load: time.sleep(0.001)
		RoverProcess.messageTrigger(self, message)
		with self.dataSem:
			self.data.update(message)
	
	def cleanup(self):
		RoverProcess.cleanup(self)
		self.listener.close()

