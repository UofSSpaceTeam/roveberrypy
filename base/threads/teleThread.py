import threading
from Queue import Queue
import math
from time import strftime


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
		self.roll = 0
		self.pitch = 0
		
		self.mx = 0
		self.my = 0
		self.mz = 0
		self.heading = 0
		
		self.vout = 0
		self.isense = 0
		
		self.gps_heading = 0
		self.lat = 0
		self.lon = 0
		
		self.laser = 0
		self.ph = 0
		self.moist = 0
		
		self.gotExpData = False
		self.towerRotation = 10
		
		
		self.log = False 
		
		#make sure log files for experiment is empty
		open("./data/laser_log.txt", "w").close()
		open("./data/ph_log.txt", "w").close()
		open("./data/moist_log.txt", "w").close()
		

	def run(self):
		while True:
			while not self.mailbox.empty():
				data = self.mailbox.get()
				print data
				try:
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
						self.pitch = self.getPitch(self.ax, self.ay, self.az)
						self.roll = self.getRoll(self.ax, self.ay, self.az)
					if "mag" in data:
						self.mx = data["mag"][0]
						self.my = data["mag"][1]
						self.mz = data["mag"][2]
						self.heading = getHeading(self.mx, self.my)
					if "heading" in data:
						self.gps_heading = data["heading"]
					if "vout" in data:
						self.vout = data["vout"]
					if "isense" in data:
						self.isense = data["isense"]
					if "laser" in data:
						self.gotExpData = True
						self.laser = data["laser"]
					if "ph" in data:
						self.gotExpData = True
						self.ph = data["ph"]
					if "moist" in data:
						self.gotExpData = True
						self.moist = data["moist"]
					if "teleGPS" in data:
						self.lat = data["teleGPS"][0]
						self.lon = data["teleGPS"][1]
					if "rotation" in data:
						self.towerRotation = data["rotation"]
						self.parent.updateTowerPos(self.towerRotation)
					
					if self.log and self.gotExpData:
						with open("./data/read_log.txt", "a") as rlog:
							rlog.write(strftime("%Y-%m-%d %H:%M:%S\n"))
							rlog.write("lat: %f lon: %f\n" %(self.lat, self.lon))
							rlog.write("laser: %f moisture: %f ph: %f\n" %(self.laser, self.moist, self.ph))
							rlog.write("\n")
						
						with open("./data/laser_log.txt", "a") as llog:
							llog.write(str(self.laser))
							llog.write(" ")
						
						with open("./data/moist_log.txt", "a") as mlog:
							mlog.write(str(self.moist))
							mlog.write(" ")
							
						with open("./data/ph_log.txt", "a") as plog:
							plog.write(str(self.ph))
							plog.write(" ")
							
						self.gotExpData = False
				except: 
					print ("mailbox error")


					
					
	def stop(self):
		self._Thread__stop()

	def getHeading(self, hx, hy):

		if hy > 0 :
			heading = 90 -  (atan(hx / hy) * (180 / PI));
		elif hy < 0:
			heading = 270 - (atan(hx / hy) * (180 / PI));
		else: 
			hy = 0
		if (hx < 0):
			heading = 180;
		else:
			heading = 0;

		#declination for Saskatoon
		#heading = heading + 10.65;
		#declination for Hanksvill 
		heading = heading + 10.90

		if (heading >= 360): 
			heading = heading - 360;   
		
		return heading
		
		
	def getPitch(self, x, y, z):
		pitch = math.atan2(x, math.sqrt(y * y) + (z * z))
		pitch *= 180.0 / math.pi
		return pitch

	def getRoll(self, x, y, z):
		roll = math.atan2(y, math.sqrt(x * x) + (z * z))
		roll *= 180.0 / math.pi
		return roll

		

