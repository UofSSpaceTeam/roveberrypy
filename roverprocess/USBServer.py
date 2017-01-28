from .RoverServer import RoverServer

from serial.tools import list_ports
import serial
import time
from .motor.interface import *
from ctypes import *
from serial.threaded import *
from  multiprocessing import BoundedSemaphore
import pyvesc

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

	def setup(self, args):
		self.IDList = {}
		self.DeviceList = []
		self.semList = {}
		ports = list_ports.comports()
		for port in ports:
			if port.device == '/dev/ttyS0' or port.device == '/dev/ttyAMA0':
				#ignore first linux serial port
				continue
			self.reqSubscription(port)

	def loop(self):
		print(self.IDList)
		time.sleep(1)

	def messageTrigger(self, message):
		# RoverProcess.messageTrigger(self, message)
		# print(self.IDList)
		print(message)
		if list(message.keys())[0] in self.IDList:
			for device in self.IDList[list(message.keys())[0]]:
				with serial.Serial(device, baudrate=BAUDRATE, timeout=1) as ser:
					ser.write(pyvesc.encode(message[list(message.keys())[0]]))

	def reqSubscription(self, port):
		with serial.Serial(port.device, baudrate=BAUDRATE, timeout=1) as ser:

			payload = [36]
			msg = makeVESCPacket(payload, len(payload))
			ser.write(msg)

			s = parseVESCPacket(ser.readline())
			if s not in self.IDList:
				self.IDList[s] = []
				self.subscribe(s)
			self.IDList[s].append(port.device)
			self.DeviceList.append(port.device)
			self.semList[port.device] = BoundedSemaphore()
			ser.reset_input_buffer()
			self.spawnThread(self.listenToDevice, port=port.device)

	def listenToDevice(self, **kwargs):
		with serial.Serial(kwargs["port"], baudrate=BAUDRATE, timeout = 0.1) as ser:
			while not self.quit:
				self.semList[kwargs["port"]].acquire()
				if ser.in_waiting > 0:
					print(ser.readline())
				self.semList[kwargs["port"]].release()
				time.sleep(0.005)
