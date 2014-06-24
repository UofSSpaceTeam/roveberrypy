import socket

class MastClient: # class for mast control
	def __init__(self, IP, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.IP = IP
		self.port = port
		self.commandMastCamera = "#MC"
	
	def connect(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.settimeout(1.0)
		try:
			self.socket.connect((self.IP, self.port))
		except:
			pass
	
	def sendData(self, x, y):
		try:
			self.socket.send(self.commandMastCamera + chr(x + 2) + chr(y + 2))
			#print x
			#print y
		except socket.error as e:
			pass # change to pass when working
	
	def test(self):
		try:
			self.socket.settimeout(0.05)
			self.socket.send("TST")
			return True
		except:
			return False

