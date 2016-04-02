import socket
import serial
import time

class PiksiRoverSatObs(object):
	def __init__(self, serport, serbaud, udpaddr, udpport):
		self._serport = serport
		self._serbaud = serbaud
		self._udpaddr = udpaddr
		self._udpport = udpport
		self._satobs_thread = threading.Thread(target=self._satobs_bridge)
		self._satobs_thread.daemon = True
		
	def __enter__(self):
		self.start()
	
	def __exit__(self):
		self.stop()
	
	def start(self):
		self._running = True
		self._satobs_thread.start()
	
	def stop(self):
		self._running = False
		self._satobs_thread.join(1)
	
	def _satobs_bridge(self):
		ser = serial.Serial(self._serport, self._serbaud)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((self._udpaddr, self._udpport))
		while self._running:
			data, addr = sock.recvfrom(1024)
			if data:
				ser.write(data)
		if ser.isopen():
			ser.close()
	
	def is_alive(self):
		return self._satobs_thread.is_alive()
			
	_serport = None
	_serbaud = None
	_udpaddr = None
	_udpport = None
	_running = False
	_satobs_thread = None