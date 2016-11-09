from .RoverProcess import RoverProcess

from serial.tools import list_ports
import serial
import time

class USBServer(RoverProcess):

	def getSubscribed(self):
		return ["TestIn", "TestOut", "wheel1", "whee2",
				"wheel3", "wheel4", "wheel5", "wheel6"]


	def setup(self, args):
		self.IDList = {b"100": "test"}
		self.DeviceList = {"test": None}
		self.InList ={"test":"TestIn"}
		self.OutList = {"test": "TestOut"}
		ports = list_ports.comports()
		for port in ports:
			with serial.Serial(port.device, timeout=1) as ser:
				ser.write(b'ID')
				s = ser.read(100)
				print(s)
				if s in self.IDList.keys():
					self.DeviceList[s] = port.device


	def loop(self):
		for key, value in self.DeviceList.items():
			with serial.Serial(value, timeout = 1) as ser:
				ser.write(b'test')
				s = ser.read(100)
				self.publish(self.OutList[key], s)
				print(s)

	def on_TestIn(self, message):
		port = self.DeviceList["test"]
		with serial.Serial(port, timeout = 1) as ser:
			print(message)
			ser.write(message)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(message)
		if "wheel1" in message:
			#forwared to appropriate device
			pass
		elif "wheel2" in message:
			#forwared to appropriate device
			pass
		elif "wheel3" in message:
			#forwared to appropriate device
			pass
		elif "wheel4" in message:
			#forwared to appropriate device
			pass
		elif "wheel5" in message:
			#forwared to appropriate device
			pass
		elif "wheel6" in message:
			#forwared to appropriate device
			pass

