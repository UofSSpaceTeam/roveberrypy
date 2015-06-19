from roverprocess import RoverProcess

import time
from threading import Thread
from multiprocessing import BoundedSemaphore
import json
import socket

class JsonServer(RoverProcess):

	class ListenThread(Thread):
		def __init__(self, listener, uplink):
			Thread.__init__(self)
			self.listener = listener
			self.uplink = uplink
			self.address = None
		
		def run(self):
			while True:
					jsonData, address = self.listener.recvfrom(4096)
					data = byteify(json.loads(jsonData))
					assert isinstance(data, dict)
					if "baseAddress" in data:
						with self.addressSem:
							self.sendAddress = data["baseAddress"]
					self.uplink.put(data)
		
		# Thanks, Mark Amery of stackoverflow!
		def byteify(input):
			if isinstance(input, dict):
				return(
						{byteify(key): byteify(value)
						for key, value in input.iteritems()})
			elif isinstance(input, list):
				return [byteify(element) for element in input]
			elif isinstance(input, unicode):
				return input.encode('utf-8')
			else:
				return input
	
	
	def setup(self, args):
		self.port = args["port"]
		self.sendPeriod = args["sendPeriod"]
		self.data = {}
		self.dataSem = BoundedSemaphore()
		self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.listener.bind(("", self.port))
		self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sendAddress = None
		self.addressSem = BoundedSemaphore()
		receiver = JsonServer.ListenThread(self.listener, self.uplink)
		receiver.daemon = True
		receiver.start()
	
	def loop(self):
		if self.data:
			with self.dataSem:
				jsonData = json.dumps(self.data)
				with self.addressSem:
					if self.sendAddress:
						self.sender.sendto(jsonData, self.sendAddress)
				self.data = {}
		time.sleep(self.sendPeriod)
	
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		with self.dataSem:
			self.data.update(message)
	
	def cleanup(self):
		RoverProcess.cleanup(self)
		self.listener.close()

