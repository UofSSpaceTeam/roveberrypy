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
		self.log(self.IDList)
		time.sleep(1)

	def messageTrigger(self, message):
		if message.key in self.IDList:
			for device in self.IDList[message.key]:
				with serial.Serial(device, baudrate=BAUDRATE, timeout=1) as ser:
					buff = pyvesc.encode(message.data)
					self.log(buff)
					ser.write(buff)

	def reqSubscription(self, port):
		with serial.Serial(port.device, baudrate=BAUDRATE, timeout=0.5) as ser:
			s = None
			errors = 0
			while errors <= 4: # try reading 4 times
				try:
					req = pyvesc.ReqSubscription('t')
					ser.write(pyvesc.encode(req))
					buff = ser.readline()
					self.log(buff, "DEBUG")
					(msg, _) = pyvesc.decode(buff)
					s = msg.subscription
					break # parseVESCPacket didn't fail
				except:
					errors += 1 # got another bad packet
					self.log("Got bad packet", "WARNING")
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
					try:
						buff = ser.readline()
						(msg, _) = pyvesc.decode(buff)
						self.log(buff, "DEBUG")
						self.publish(msg.__class__.__name__, msg)
					except:
						self.log("Failed to parse message", "ERROR")
				self.semList[kwargs["port"]].release()
				time.sleep(0.005)
