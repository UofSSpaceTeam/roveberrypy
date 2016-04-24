from multiprocessing import Process, BoundedSemaphore
import threading, sys

class RoverProcess(Process):
	class ReceiverThread(threading.Thread):
		def __init__(self, downlink, state, sem, parent):
			threading.Thread.__init__(self)
			self.downlink = downlink
			self._state = state
			self._stateSem = sem
			self._parent = parent
		
		def run(self):
			while True:
				data = self.downlink.get()
				assert isinstance(data, dict)
				with self._stateSem:
					self._state.update(data)
				self._parent.messageTrigger(data)
		
	def __init__(self, **kwargs):
		Process.__init__(self)
		self.uplink = kwargs["uplink"]
		self.downlink = kwargs["downlink"]
		self._state = dict()
		self._stateSem = BoundedSemaphore()
		self._args = kwargs
		self.load = True
		
	def getSubscribed(self):
		pass
		
	def run(self):
		receiver = RoverProcess.ReceiverThread(
			self.downlink, self._state, self._stateSem, self)
		receiver.start()
		try:
			self.setup(self._args)
			while True:
				self.loop()
		except KeyboardInterrupt:
			self.cleanup()
			sys.exit(0)
		except:
			self.cleanup()
			raise
	
	def setup(self, args):
		pass
	
	def loop(self):
		pass
	
	def messageTrigger(self, message):
		if "quit" in message:
			print "Got cleanup"
			self.cleanup()
			sys.exit(0)
	
	def getShared(self, key):
		with self._stateSem:
			if key in self._state:
				return self._state[key]
			else:
				return None
	
	def setShared(self, key, value):
		with self._stateSem:
			self._state.update({key:value})
		self.uplink.put({key:value})
	
	def cleanup(self):
		for thread in threading.enumerate():
				if thread is not threading.current_thread():
					thread._Thread__stop()
					thread._Thread__delete()

