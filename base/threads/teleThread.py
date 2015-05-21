import threading
from Queue import Queue

class TeleThread(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.parent = parent
		self.mailbox = Queue()
		
		self.gx = 0
		self.gy = 0
		self.gz = 0
		
		self.ax = 0
		self.ay = 0
		self.gz = 0
		
		self.pitch = 0
		self.roll = 0
		
		self.aroll = 0
		self.apitch = 0
		
		self.vout = 0
		self.isense = 0
		
		self.heading = 0

	def run(self):
		while True:
			while not self.mailbox.empty():
				data = self.mailbox.get()
				
				if "pitch" in data:
					self.pitch = data["pitch"]
				if "roll" in data:
					self.roll = data["roll"]
				if "gx" in data:
					self.gx = data["gx"]
				if "gy" in data:
					self.gy = data["gy"]
				if "gz" in data:
					self.gz = data["gz"]
				if "ax" in data:
					self.ax = data["ax"]
				if "ay" in data:
					self.ay = data["ay"]
				if "az" in data:
					self.az = data["az"]
				if "heading" in data:
					self.heading = data["heading"]
				if "aroll" in data:
					self.aroll = data["aroll"]
				if "apitch" in data:
					self.apitch = data["apitch"]
				if "vout" in data:
					self.vout = data["vout"]
				if "isense" in data:
					self.isense = data["isense"]
					
	def stop(self):
		self._Thread__stop()
