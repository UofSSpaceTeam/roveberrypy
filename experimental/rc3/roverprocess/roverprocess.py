from multiprocessing import Process, BoundedSemaphore
import threading

class RoverProcess(Process):
	class ReceiverThread(threading.Thread):
		def __init__(self, downlink, state, sem, parent):
			threading.Thread.__init__(self)
			self.downlink = downlink
			self.state = state
			self.sem = sem
			self.parent = parent
		
		def run(self):
			while True:
				data = self.downlink.get()
				assert isinstance(data, dict)
				with self.sem:
					self.state.update(data)
				RoverProcess.messageTrigger(self.parent, data)
		
	def __init__(self, **kwargs):
		Process.__init__(self)
		self.uplink = kwargs["uplink"]
		self.downlink = kwargs["downlink"]
		self.state = dict()
		self.sem = BoundedSemaphore()
		
	def run(self):
		print self.__name__ + "started"
		receiver = RoverProcess.ReceiverThread(
			self.downlink, self.state, self.sem, self)
		receiver.daemon = True
		receiver.start()
		try:
			self.setup()
			while True:
				self.loop()
		except:
			self.cleanup()
			raise
	
	def setup(self):
		pass
	
	def loop(self):
		pass
	
	def messageTrigger(self, message):
		if "quit" in message:
			raise KeyboardInterrupt
	
	def get(self, key):
		with self.sem:
			if key in self.state:
				return self.state[key]
			else:
				return None
	
	def set(self, key, value):
		with self.sem:
			self.state.update({key:value})
		self.uplink.put({key:value})
	
	def cleanup(self):
		for thread in threading.enumerate():
				if thread is not threading.main_thread():
					thread._Thread__stop()
					thread._Thread__delete()

