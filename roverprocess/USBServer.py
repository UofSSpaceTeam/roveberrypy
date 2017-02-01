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
		if list(message.keys())[0] in self.IDList:
			for device in self.IDList[list(message.keys())[0]]:
				with serial.Serial(device, baudrate=BAUDRATE, timeout=1) as ser:
					ser.write(pyvesc.encode(message[list(message.keys())[0]]))

	def reqSubscription(self, port):
		with serial.Serial(port.device, baudrate=BAUDRATE, timeout=1) as ser:
			req = pyvesc.ReqSubscription()
			ser.write(pyvesc.encode(req))

			errors = 0
			while errors <= 4: # try reading 4 times
				try:
					#TODO, vesc firmware seems to not use quite the
					#      same packet format when it prints messages back
					#      (no packet id or checksum as far as I can tell)
					buff = ser.readline()
					s = parseVESCPacket(buff)
					break # parseVESCPacket didn't fail
				except:
					errors += 1 # got another bad packet
					print("Got bad packet")
			if not s:
				return # failed to get a good packet, abort
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
