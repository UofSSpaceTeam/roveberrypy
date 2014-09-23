import socket
import time
	
class DriveClient: # class for drive control
	def __init__(self, IP, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.IP = IP
		self.port = port
		self.commandOneStickData = "#D1"
		self.commandTwoStickData = "#D2"
		self.commandRoverStop = "#DS"
		self.commandRoverDig = "#DD"
	
	def connect(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.settimeout(1.0)
		try:
			self.socket.connect((self.IP, self.port))
		except:
			pass
	
	def sendOneStickData(self, xAxis, yAxis, limit):
		xInt = int(xAxis * 127) + 127
		yInt = int(yAxis * 127) + 127
		try:
			self.socket.send(self.commandOneStickData + chr(xInt) + chr(yInt) + chr(limit))
		except:
			raise
			#self.stopMotors()
	
	def sendTwoStickData(self, leftAxis, rightAxis):
		leftInt = int(leftAxis * 127) + 127
		rightInt = int(rightAxis * 127) + 127
		try:
			self.socket.send(self.commandTwoStickData + chr(leftInt) + chr(rightInt))
		except:
			raise
			#self.stopMotors()
	
	def stopMotors(self):
		try:
			self.socket.send(self.commandRoverStop)
		except:
			pass
	
	def dig(self):
		try:
			self.socket.send(self.commandRoverDig)
		except:
			pass
	
	def test(self):
		try:
			self.socket.settimeout(0.05)
			self.socket.send("TST")
			return True
		except:
			return False

