import socket

class ScienceClient: # class for science experiment control
	def __init__(self, IP, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.IP = IP
		self.port = port
		self.commandRunExperiment = "#RE"
	
	def connect(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.settimeout(1.0)
		try:
			self.socket.connect((self.IP, self.port))
		except:
			pass
	
	def runExperiment(self):
		try:
			self.socket.send(self.commandRunExperiment)
		except socket.error as e:
			raise # change to pass when working
	
	def test(self):
		try:
			self.socket.settimeout(0.05)
			self.socket.send("TST")
			return True
		except:
			return False

