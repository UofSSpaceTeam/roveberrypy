from multiprocessing import Process, Queue
from threading import Thread
import json
import socket
import time

class JsonServer(Process):
	class ReceiverThread(Thread):
		def __init__(self, listener, fromServer):
			Thread.__init__(self)
			self.listener = listener
			self.fromServer = fromServer
			self.address = None
		
		def run(self):
			while True:
				try:
					jsonData, address = self.listener.recvfrom(4096)
					data = byteify(json.loads(jsonData))
					assert isinstance(data, dict)
					self.fromServer.put(data)
				except Exception as e:
					print("JsonServer: " + str(e.message))
		
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
	
	def __init__(self, port,  toServer, fromServer, sendPeriod=0.1):
		Process.__init__(self)
		self.port = port
		self.fromServer = fromServer
		self.toServer = toServer
		self.sendPeriod = sendPeriod
	
	def run(self):
		self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.listener.bind(("", self.port))
		self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sendAddress = None
		receiver = JsonServer.ReceiverThread(self.listener, self.fromServer)
		receiver.daemon = True
		receiver.start()
		while True:
			try:
				data = {}
				while not self.toServer.empty():
					data.update(self.toServer.get())
				if not data:
					continue
				if "quit" in data:
					return
				if "baseAddress" in data:
					self.sendAddress = data["baseAddress"]
				if not self.sendAddress:
					continue
				jsonData = json.dumps(data)
				self.sender.sendto(jsonData, self.sendAddress)
				time.sleep(self.sendPeriod)
			except KeyboardInterrupt:
				return
			except Exception as e:
				print("JsonServer: " + str(e.value))

