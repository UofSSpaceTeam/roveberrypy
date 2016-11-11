from .RoverProcess import RoverProcess

from serial.tools import list_ports
import serial
import time

class USBServer(RoverProcess):

	def getSubscribed(self):
		return ["TestIn", "TestOut", "wheel1", "wheel2",
				"wheel3", "wheel4", "wheel5", "wheel6"]


	def setup(self, args):
		self.IDList = {b'\x01': "test"}
		self.DeviceList = {}
		self.InList ={"test":"TestIn"}
		self.OutList = {b'\x01': "TestOut"}
		ports = list_ports.comports()
		for port in ports:
			if port.device == '/dev/ttyS0':
				continue
			with serial.Serial(port.device) as ser:
				ser.write(b'ID')
				s = ser.read(1)
				print("got Id: ", s)
				if s in self.IDList.keys():
					self.DeviceList[s] = port.device


	def loop(self):
		for key, value in self.DeviceList.items():
			try:
				with serial.Serial(value) as ser:
					ser.write(b'req')
					num_bytes = ser.read(1)
					print(num_bytes)
					s = ser.read(int.from_bytes(num_bytes, byteorder='little'))
					self.publish(self.OutList[key], s)
					print("published: ", s)
			except Exception:
				raise
		time.sleep(1)

	def on_TestIn(self, message):
		port = self.DeviceList["test"]
		with serial.Serial(port, timeout=1) as ser:
			print(message)
			ser.write(message)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
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

