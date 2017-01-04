from .RoverServer import RoverServer

from serial.tools import list_ports
import serial
import time
from .motor.interface import *
from ctypes import *
from serial.threaded import *
from  multiprocessing import BoundedSemaphore

BAUDRATE = 115200

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
	b_msg = bytes(msg)
	return b_msg


def parseVESCPacket(packet):
	msg = packet[2:2+packet[1]].decode("utf-8")
	return msg


class USBServer(RoverServer):

	def getSubscribed(self):
		return ["test", "TestIn", "TestOut", "wheel1", "wheel2",
				"wheel3", "wheel4", "wheel5", "wheel6"]

	def setup(self, args):
		self.IDList = {}
		self.DeviceList = []
		self.semList = {}
		self.InList ={"test":"TestIn"}
		self.OutList = {b'\x01': "TestOut"}
		ports = list_ports.comports()
		for port in ports:
			if port.device == '/dev/ttyS0' or port.device == '/dev/ttyAMA0':
				#ignore first linux serial port
				continue
			self.reqSubscription(port)

	def loop(self):
		print(self.DeviceList)
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
		time.sleep(1)

	def on_TestIn(self, message):
		port = self.DeviceList["test"]
		with serial.Serial(port, timeout=1) as ser:
			# print(message)
			ser.write(message)

	def messageTrigger(self, message):
		# RoverProcess.messageTrigger(self, message)
		# print(self.IDList)
		if "wheel1" in message:
			if "wheel1" in self.IDList:
				for device in self.IDList["wheel1"]:
					self.spawnThread(self.drive, port=device, speed=message["wheel1"])
					# pass
		elif "wheel2" in message:
			if "wheel2" in self.IDList:
				for device in self.IDList["wheel2"]:
					self.spawnThread(self.drive, port=device, speed=message["wheel2"])
		elif "wheel3" in message:
			if "wheel3" in self.IDList:
				for device in self.IDList["wheel3"]:
					self.spawnThread(self.drive, port=device, speed=message["wheel3"])
		elif "wheel4" in message:
			if "wheel4" in self.IDList:
				for device in self.IDList["wheel4"]:
					self.spawnThread(self.drive, port=device, speed=message["wheel4"])
		elif "wheel5" in message:
			if "wheel5" in self.IDList:
				for device in self.IDList["wheel5"]:
					self.spawnThread(self.drive, port=device, speed=message["wheel5"])
		elif "wheel6" in message:
			if "wheel6" in self.IDList:
				for device in self.IDList["wheel6"]:
					self.spawnThread(self.drive, port=device, speed=message["wheel6"])
		elif "test" in message:
			if "test" in self.IDList:
				for device in self.IDList["test"]:
					self.spawnThread(self.blink, port=device, value=message["test"])

	def reqSubscription(self, port):
		with serial.Serial(port.device, baudrate=BAUDRATE, timeout=1) as ser:

			payload = [36]
			msg = makeVESCPacket(payload, len(payload))
			ser.write(msg)

			s = parseVESCPacket(ser.readline())
			if s not in self.IDList:
				self.IDList[s] = []
			self.IDList[s].append(port.device)
			self.DeviceList.append(port.device)
			self.semList[port.device] = BoundedSemaphore()
			ser.reset_input_buffer()
			self.spawnThread(self.listenToDevice, port=port.device)

	def blink(self, **kwargs):
		self.semList[kwargs["port"]].acquire()
		with serial.Serial(kwargs["port"], baudrate=BAUDRATE, timeout = 0.1) as ser:
			payload = [1]
			payload.append(kwargs["value"])
			msg = makeVESCPacket(payload, len(payload))
			ser.write(msg)
		self.semList[kwargs["port"]].release()


	#TODO move to DriveProcess?
	def drive(self, **kwargs):
		self.semList[kwargs["port"]].acquire()
		with serial.Serial(kwargs["port"], baudrate=BAUDRATE, timeout = 0.1) as ser:
			b_cycle = pyint32tobytes(kwargs["speed"])
			payload = [8]
			payload.extend(b_cycle)
			msg = makeVESCPacket(payload, len(payload))
			ser.write(msg)
		self.semList[kwargs["port"]].release()

	def listenToDevice(self, **kwargs):
		with serial.Serial(kwargs["port"], baudrate=BAUDRATE, timeout = 0.1) as ser:
			while not self.quit:
				self.semList[kwargs["port"]].acquire()
				if ser.in_waiting > 0:
					print(ser.readline())
				self.semList[kwargs["port"]].release()
				time.sleep(0.005)
