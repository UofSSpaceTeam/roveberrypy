from roverprocess import RoverProcess

import serial
import socket

class OculusProcess(RoverProcess):
	
	def setup(self, args):
		self.serial = serial.Serial(args["serialPort"], 9600)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.bind(("", args["udpPort"]))
	
	def loop(self):
		self.serial.write(self.socket.recvfrom(1024)[0])
	
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
	
	def cleanup(self):
		RoverProcess.cleanup(self)
