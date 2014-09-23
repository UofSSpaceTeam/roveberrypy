import socket
import struct
	
class GPSClient: # class for getting position data
	def __init__(self, IP, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.IP = IP
		self.port = port

	def connect(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.settimeout(1.0)
		try:
			self.socket.connect((self.IP, self.port))
		except:
			pass

	def getPosition(self):
		try:
			self.socket.settimeout(0.3)
			packet = self.socket.recv(256)
			data = struct.unpack("!ffffff", packet)
			return data
		except:
			return None
	
	def test(self):
		try:
			self.socket.settimeout(0.05)
			self.socket.send("TST")
			return True
		except:
			return False

