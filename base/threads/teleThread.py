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
		self.az = 0
		
		self.pitch = 0
		self.roll = 0
		
		self.vout = 0
		self.isense = 0
		
		self.heading = 0
		
		self.dataSum = [0,0,0,0,0,0,0,0,0]

	def run(self):
		while True:
			while not self.mailbox.empty():
				data = self.mailbox.get()
				if "pitch" in data:
					self.pitch = data["pitch"]
				if "roll" in data:
					self.roll = data["roll"]
				if "gyro" in data:
					self.gx = data["gyro"][0]
					print("gx")
					self.gy = data["gyro"][1]
					print("gy")
					self.gz = data["gyro"][2]
					print("gz")
				if "accel" in data:
					self.ax = data["accel"][0]
					print("az")
					self.ay = data["accel"][1]
					print("ay")
					self.az = data["accel"][2]
					print("az")
				if "heading" in data:
					self.heading = data["heading"]
				if "vout" in data:
					self.vout = data["vout"]
					print("vout")
				if "isense" in data:
					print("isense")
					self.isense = data["isense"]
					
	def stop(self):
		self._Thread__stop()
		
