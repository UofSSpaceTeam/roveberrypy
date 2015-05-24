import threading
import socket
import struct
import serial

class CameraThread(threading.Thread):
	def __init__(self, parent, port):
		threading.Thread.__init__(self)
		self.name = "cameraThread"
		self.parent = parent
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(("", port))
		self.arduino = serial.Serial("/dev/ttyAMA0", bytesize = 8,
			parity = 'N', stopbits = 1)
		self.arduino.baudrate = 9600
		self.arduino.timeout = 0.2

	def run(self):
		while True:
			inData, address = self.socket.recvfrom(1024)
			cmd = struct.unpack("BBBBBB", inData)
			print str(cmd)
			self.arduino.write(inData);

