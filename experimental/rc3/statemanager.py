from threading import Thread, BoundedSemaphore
from multiprocessing import Queue

class StateManager:
	class WorkerThread(Thread):
		def __init__(self, inQueue, state, observerMap, sem):
			Thread.__init__(self)
			self.inQueue = inQueue
			self.state = state
			self.observerMap = observerMap
			self.sem = sem
		
		def run(self):
			while True:
				data = self.inQueue.get()
				assert isinstance(data, dict)
				with self.sem:
					self.state.update(data)
					for key in data:
						self.notifyObservers(key)
		
		def notifyObservers(self, key):
			if key in observerMap:
				for downlinkQueue in observerMap[key]:
					downlinkQueue.put({key:state[key]})

	def __init__(self):
		self.sem = BoundedSemaphore()
		self.state = dict()
		self.observerMap = dict()
		self.downlinkQueues = []
	
	def terminate(self):
		for queue in self.downlinkQueues:
			queue.put({"quit":"True"})
		self.downlinkQueues = []
	
	def dumpState(self):
		out = ""
		with self.sem:
			for key in self.state:
				out += str(key) + ":" + str(self.state[key]) + "\n"
		return out
	
	def getUplinkQueue(self):
		uplinkQueue = Queue()
		worker = StateManager.WorkerThread(
			uplinkQueue, self.state, self.observerMap, self.sem)
		worker.daemon = True
		worker.start()
		return uplinkQueue
	
	def getDownlinkQueue(self):
		queue = Queue()
		self.downlinkQueues.append(queue)
		return queue
	
	def addObserver(self, key, downlinkQueue):
		assert isinstance(downlinkQueue, Queue)
		with self.sem:
			if key not in observerMap:
				observerMap[key] = list()
			if downlinkQueue not in observerMap[key]:
				observerMap[key].append(downlinkQueue)
	
	def removeObserver(self, key, downlinkQueue):
		assert isinstance(downlinkQueue, Queue)
		with self.sem:
			if key in observerMap and downlinkQueue in observerMap[key]:
				observerMap[key].remove(downlinkQueue)
				if not observerMap[key]: # empty list
					del observerMap[key]
	
	def dumpObservers(self):
		out = ""
		with self.sem:
			for key in self.observerMap:
				out += str(key) + ":"
				out += str(len(self.observerMap[key])) + "\n"
		return out

