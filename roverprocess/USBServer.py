from .RoverProcess import RoverProcess

from serial.tools import list_ports
import serial
import time

class USBServer(RoverProcess):

	def getSubscribed(self):
		return ["TestIn", "TestOut", "wheel1", "wheel2",
				"wheel3", "wheel4", "wheel5", "wheel6"]


	def setup(self, args):
		self.IDList = {}
		self.DeviceList = []
		self.InList ={"test":"TestIn"}
		self.OutList = {b'\x01': "TestOut"}
		ports = list_ports.comports()
		for port in ports:
			if port.device == '/dev/ttyS0':
				#ignore first linux serial port
				continue
			with serial.Serial(port.device) as ser:
				ser.write(b'subs')
				num_bytes = ser.read(1)
				s = ser.read(int.from_bytes(num_bytes, byteorder='little'))
				print("got sub: ", s)
				if s not in self.IDList:
					self.IDList[s] = []
				self.IDList[s].append(port.device)
				self.DeviceList.append(port.device)
				# if s in self.IDList.keys():
				# 	self.DeviceList[s] = port.device


	def loop(self):
		for port in self.DeviceList:
			try:
				with serial.Serial(port) as ser:
					ser.write(b'req')
					num_bytes = ser.read(1)
					print(num_bytes)
					s = ser.read(int.from_bytes(num_bytes, byteorder='little'))
					# self.publish(self.OutList[key], s)
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

