from .RoverServer import RoverServer

from serial.tools import list_ports
import serial
import time
from ctypes import *
from serial.threaded import *
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
		ports = list_ports.comports()
		for port in ports:
			if port.device == '/dev/ttyS0' or port.device == '/dev/ttyAMA0'\
						or port.device == '/dev/ttyUSB0':
							#ignore first linux serial port and Piksi gps
				continue
			# In pyserial, port.device is a string of the path to the device
			self.reqSubscription(port.device)

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
		if device.in_waiting > 0:
			buff = device.readline()
			(msg, _) = pyvesc.decode(buff)
			self.log("Got: "+str(buff), "DEBUG")
			return (msg.__class__.__name__, msg)
		else:
			return None

	def getSubscription(self, device):
		s = None
		errors = 0
		while errors < 4: # try reading 4 times
			try:
				req = pyvesc.ReqSubscription('t')
				device.write(pyvesc.encode(req))
				buff = device.readline()
				self.log(buff, "DEBUG")
				(msg, _) = pyvesc.decode(buff)
				s = msg.subscription
				break # parseVESCPacket didn't fail
			except:
				errors += 1 # got another bad packet
				self.log("Got bad packet", "WARNING")
			device.reset_input_buffer()
		return s

	def getDevice(self, port):
		return serial.Serial(port, baudrate=BAUDRATE, timeout=1)

