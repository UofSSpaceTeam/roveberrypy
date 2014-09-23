import socket
import time

class CameraClient: # class to handle camera feeds	
	def __init__(self, IP, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.IP = IP
		self.port = port
		self.commandCameraStart = "#CS"
		self.commandCameraEnd = "#CE"
		self.commandCameraPicture = "#CP"
	
	def connect(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.settimeout(1.0)
		try:
			self.socket.connect((self.IP, self.port))
		except:
			pass
	
	def startCamera(self):
		try:
			self.socket.send(self.commandCameraStart)
		except:
			pass
	
	def stopCamera(self):
		try:
			self.socket.send(self.commandCameraEnd)
		except:
			pass

	def takePicture(self):
		try:
			self.socket.send(self.commandCameraPicture)
		except:
			pass

	def test(self):
		try:
			self.socket.settimeout(0.05)
			self.socket.send("TST")
			return True
		except:
			return False

