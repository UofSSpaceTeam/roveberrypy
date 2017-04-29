from .RoverServer import RoverServer

from serial.tools import list_ports
import serial
import time
from ctypes import *
from serial.threaded import *
from  multiprocessing import BoundedSemaphore
import pyvesc

BAUDRATE = 115200
""" The baudrate to use for serial communication."""

class USBServer(RoverServer):
	""" Forwards RoverMessages to devices connected to USB.

	The USBServer first polls all connected devices to see what messages
	they are subscribed to. The server then subscribes to those messages.
	When those messages are published by other processes, the USBServer
	will forward it to the appropriate device.

	The USBServer also listens for incomming messages from each device,
	and publishes them to the rest of the system for other processes.
	"""

	def setup(self, args):
		""" Initialize subscription maps and find what messages devices are susbribed to."""
		self.DeviceList = []
		ports = list_ports.comports()
		for port in ports:
			if port.device == '/dev/ttyS0' or port.device == '/dev/ttyAMA0':
				#ignore first linux serial port
				continue
			self.reqSubscription(port)

	def loop(self):
		""" Just print out the subscriptions."""
		self.log(self.subscriberMap)
		time.sleep(1)

	def send_cmd(self, message, device):
		with serial.Serial(device, baudrate=BAUDRATE, timeout=1) as ser:
			buff = pyvesc.encode(message.data)
			self.log(buff, "DEBUG")
			ser.write(buff)

	def read_cmd(self, device):
		with serial.Serial(device, baudrate=BAUDRATE, timeout=0.1) as ser:
			if ser.in_waiting > 0:
				buff = ser.readline()
				(msg, _) = pyvesc.decode(buff)
				self.log(buff, "DEBUG")
				return (msg.__class__.__name__, msg)
			else:
				return None

	def reqSubscription(self, port):
		""" Request susbscriptions from a device.

		If we get an invalid response, try again up to 4 times.
		Subscribe to the message if we're not subscribed already.
		Also store the device for later. Finally, spin up a thread
		to listen for incomming messages from the device.
		"""
		with serial.Serial(port.device, baudrate=BAUDRATE, timeout=0.5) as ser:
			s = None
			errors = 0
			while errors < 4: # try reading 4 times
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
			if s not in self.subscriberMap:
				self.subscriberMap[s] = []
				self.subscribe(s)
			self.subscriberMap[s].append(port.device)
			self.DeviceList.append(port.device)
			self.semList[port.device] = BoundedSemaphore()
			ser.reset_input_buffer()
			self.spawnThread(self.listenToDevice, port=port.device)

