from RoverProcess import RoverProcess

from serial.tools import list_ports
import serial
import time

class USBServer(RoverProcess):
	IDList = {b"100": "test"}
	DeviceList = {"test": None}
	InList ={"test":"TestIn"}
	OutList = {"test": "TestOut"}
	
	def getSubscribed(self):
		return ["TestIn", "TestOut"]
		
	def setup(self, args):
		ports = list_ports.comports()
		for port in ports:
			with serial.Serial(port.device, timeout=1) as ser:
				ser.write(b'ID')
				s = ser.read(100)
				print(s)
				if s in IDList.keys():
					DeviceList[s] = port.device
	
	
	def loop(self):
		for key, value in DeviceList.items():
			with serial.Serial(value, timeout = 1) as ser:
				ser.write(b'test')
				s = ser.read(100)
				self.publish(OutList[key], s)
				print(s)
	def on_TestIn(self, message):
		port = DeviceList["test"]
		with serial.Serial(port, timeout = 1) as ser:
			print(message)
			ser.write(message)