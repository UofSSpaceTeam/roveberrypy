import time, sys
from multiprocessing import Process, Queue, BoundedSemaphore
from threading import Thread, current_thread

class RoverProcess(Process):
	class ReceiverThread(Thread):
		def __init__(self, downlinkQueue, state, sem, parent):
			Thread.__init__(self)
			self.downlinkQueue = downlinkQueue
			self.state = state
			self.sem = sem
			self.parent = parent
		
		def run(self):
			while True:
				data = self.downlinkQueue.get()
				assert isinstance(data, dict)
				with self.sem:
					self.state.update(data)
				RoverProcess.messageTrigger(self.parent, data)
		
	def __init__(self, uplinkQueue, downlinkQueue):
		Process.__init__(self, target=self.run)
		self.uplinkQueue = uplinkQueue
		self.downlinkQueue = downlinkQueue
		self.state = dict()
		self.sem = BoundedSemaphore()
		
	def run(self):
		receiver = RoverProcess.ReceiverThread(
			self.downlinkQueue, self.state, self.sem, self)
		receiver.daemon = True
		receiver.start()
		while True:
			try:
				time.sleep(2)
			except KeyboardInterrupt:
				return
	
	def messageTrigger(self, message):
		if "quit" in message:
			print("stopping!")
	
	def get(self, key):
		with self.sem:
			if key in self.state:
				return self.state[key]
			else:
				return None
	
	def set(self, key, value):
		with self.sem:
			self.state.update({key:value})
		self.uplinkQueue.put({key:value})

