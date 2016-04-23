from threading import Thread, BoundedSemaphore
from multiprocessing import Queue

class StateManager:
	class WorkerThread(Thread):
		## threading module automatically initializes and runs worker
		def __init__(self, uplink, state, observerMap, sem):
			Thread.__init__(self)
			self.uplink = uplink
			self.state = state
			self.observerMap = observerMap
			self.stateSem = sem
		
		def run(self):
			while True:
				data = self.uplink.get()
				assert isinstance(data, dict)
				with self.stateSem:
					self.state.update(data)
					for key in data:
						self.notifyObservers(key)
		
		## Helper to send data to the registered observers defined in main.py
		def notifyObservers(self, key):
			if key in self.observerMap:
				for downlink in self.observerMap[key]:
					downlink.put({key:self.state[key]})

	
	## Main state management functions
	def __init__(self):
		self.stateSem = BoundedSemaphore()
		self.state = dict()
		self.observerMap = dict()
		self.downlinks = []
	
	def terminateState(self):
		for queue in self.downlinks:
			queue.put({"quit":"True"})
		self.downlinks = []
	
	def dumpState(self):
		out = ""
		with self.stateSem:
			for key in self.state:
				out += str(key) + ":" + str(self.state[key]) + "\n"
		return out
	
	def getUplink(self):
		uplink = Queue()
		worker = StateManager.WorkerThread(
			uplink, self.state, self.observerMap, self.stateSem)
		worker.daemon = True
		worker.start()
		return uplink
	
	def getDownlink(self):
		downlink = Queue()
		self.downlinks.append(downlink)
		return Queue()
	
	def addObserver(self, key, downlink):
		with self.stateSem:
			if key not in self.observerMap:
				self.observerMap[key] = list()
			if downlink not in self.observerMap[key]:
				self.observerMap[key].append(downlink)
	
	def dumpObservers(self):
		out = ""
		with self.stateSem:
			for key in self.observerMap:
				out += str(key) + ":"
				out += str(len(self.observerMap[key])) + "\n"
		return out

