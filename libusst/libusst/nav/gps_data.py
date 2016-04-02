from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client import Handler, Framer

class PiksiData(object):
	def __init__(self, port, baud):
		self._port = port
		self._baud = baud
		self._dat = {}
	
	def update(self, msg):
		self._dat[msg.msg_type] = msg
		
	def __enter__(self):
		self.start()
		
	def __exit__(self):
		self.stop()
	
	def start(self):
		self._ser = PySerialDriver(self._port, self._baud)
		self._link = Handler(Framer(self._ser.read, self._ser.write))
		self._link.add_callback(update, DATA_MSG_ID)
		self._link.start()
	
	def stop(self):
		self._link.stop()
		self._ser.__exit__()
		
	def is_alive(self):
		return self._link.is_alive()
		
	def lat(self):
		pass
	def lon(self):
		pass
	def alt(self):
		pass
	def status(self):
		pass
		
	_port = None
	_baud = None
	_dat = None