from .RoverProcess import RoverProcess

from serial.tools import list_ports
import serial
import time
from .motor.interface import *
from ctypes import *

def makeVESCPacket(payload, len):
	crc = pycrc16(payload, len)
	msg = []
	if len <= 256:
		msg.append(2)
		msg.append(len)
	else:
		msg.append(3)
		msg.append(int(len/(2**8)))
		msg.append(len&0xFF)
	msg.extend(payload)

	msg.append(int(crc.value/(2**8)))

	msg.append(crc.value&0xFF)
	msg.append(3)
	# print(msg)
	b_msg = bytes(msg)
	# print(b_msg)
	return b_msg

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
			self.reqSubscription(port)


	def loop(self):
		ports = list_ports.comports()
		for port in ports:
			if port.device == "/dev/ttyS0":
				continue
			with serial.Serial(port.device, timeout = 1) as ser:
				self.drive(ser, 15000)
		# for port in self.DeviceList:
		# 	try:
		# 		with serial.Serial(port) as ser:
		# 			ser.write(b'req')
		# 			num_bytes = ser.read(1)
		# 			print(num_bytes)
		# 			s = ser.read(int.from_bytes(num_bytes, byteorder='little'))
		# 			# self.publish(self.OutList[key], s)
		# 			print("published: ", s)
		# 	except Exception:
		# 		raise
		time.sleep(0.05)

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

	def reqSubscription(self, port):
		with serial.Serial(port.device, timeout=1) as ser:
			ser.write(b'subs')
			num_bytes = ser.read(1)
			s = ser.read(int.from_bytes(num_bytes, byteorder='little'))
			print("got sub: ", s)
			if s not in self.IDList:
				self.IDList[s] = []
			self.IDList[s].append(port.device)
			self.DeviceList.append(port.device)

	def drive(self, ser, speed):
		b_cycle = pyint32tobytes(speed)
		payload = [8]
		payload.extend(b_cycle)
		msg = makeVESCPacket(payload, len(payload))
		ser.write(msg)
		ser.readline()
		#ser.write(SendPacket([4],1))
		data = ser.readline()
