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
		
		self.mx = 0
		self.my = 0
		self.mz = 0
		
		self.vout = 0
		self.isense = 0
		
		self.heading = 0
		
		self.laser = 0
		self.ph = 0
		self.moist = 0

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
					self.gy = data["gyro"][1]
					self.gz = data["gyro"][2]
				if "accel" in data:
					self.ax = data["accel"][0]
					self.ay = data["accel"][1]
					self.az = data["accel"][2]
				if "mag" in data:
					self.mx = data["mag"][0]
					self.my = data["mag"][1]
					self.mz = data["mag"][2]
				if "heading" in data:
					self.heading = data["heading"]
				if "vout" in data:
					self.vout = data["vout"]
				if "isense" in data:
					self.isense = data["isense"]
				if "laser" in data:
					self.laser = data["laser"]
				if "ph" in data:
					self.ph = data["ph"]
				if "moist" in data:
					self.isense = data["moist"]
					
	def stop(self):
		self._Thread__stop()
		
		
	def getHeading(self, hx, hy):

		if hy > 0 :
			heading = 90 -  (atan(hx / hy) * (180 / PI));
                elif  hy < 0:
			heading = 270 - (atan(hx / hy) * (180 / PI));
		else: 
			hy = 0
		if (hx < 0):
			heading = 180;
		else:
			heading = 0;

		#declination for Saskatoon
		heading = heading + 10.65;
		#declination for Hanksvill 
		#heading = heading + 10.90

		if (heading >= 360): 
			heading = heading - 360;   
		
		return heading
		
