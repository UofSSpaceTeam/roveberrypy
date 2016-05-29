from RoverProcess import RoverProcess

import time, struct, string

class ControlMode:
	CURRENT = 0x00
	BRAKE = 0x01
	RPM = 0x02
	

class DriveProcess(RoverProcess):

	def getSubscribed(self):
		# Returns a dictionary of lists for all the incoming (self) and outgoing (server) subscriptions
		return {
				"self" : ["m1Stats", "axes"],
				"json" : [],
				"can" : ["769", "1", "257"],
				"web" : []
				}

	def expo(self, val):
		return val**3

        def setDuty(self, val, id):
                DUTY = 0
		val = int(val*100000)
                buffer = [chr((val >> 32) & 0xFF), chr((val >> 16) & 0xFF), chr((val >> 8) & 0xFF), chr((val) & 0xFF)]
                key = id | ((DUTY << 8) & 0xFFFFFFFF)
                self.setShared(str(key), string.join(buffer, ""))

	# Sets in mA
	def setCurrent(self, val, id):
		CURRENT = 1
		val = int(val*10000)
		print val
                buffer = [chr((val >> 32) & 0xFF), chr((val >> 16) & 0xFF), chr((val >> 8) & 0xFF), chr((val) & 0xFF)]
                key = id | ((CURRENT << 8) & 0xFFFFFFFF)
      		self.setShared(str(key), string.join(buffer, ""))

	def setBrake(self, val, id):
		BRAKE = 2
                buffer = [chr((val >> 32) & 0xFF), chr((val >> 16) & 0xFF), chr((val >> 8) & 0xFF), chr((val) & 0xFF)]
                key = id | ((BRAKE << 8) & 0xFFFFFFFF)
                self.setShared(str(key), string.join(buffer, ""))		

        def setRPM(self, val, id):
                val = int(val*-40000)
		RPM = 3
                buffer = [chr((val >> 32) & 0xFF), chr((val >> 16) & 0xFF), chr((val >> 8) & 0xFF), chr((val) & 0xFF)]
                key = id | ((RPM << 8) & 0xFFFFFFFF)
		self.setShared(str(key), string.join(buffer, ""))

	def setup(self, args):
		self.m1Stats = (0,0,0)
		self.m1RPM = 0
		self.m1Current = 0
		self.m1Count = 0
		self.m1Temp = 0
		self.rpm = 0
		self.datalist = []
		self.maxThrottle = 36000
		self.exponential = 2
		self.mode = ControlMode.RPM
	
	def loop(self):
		#self.m1RPM = self.m1Stats[0]
		print self.m1RPM*10, self.m1Current/10.0, self.m1Temp, self.m1Count
		#self.structtest = struct.unpack("l", self.m1Raw[0:4])
		#print self.structtest
		
		#b_array = bytearray(self.datalist[0:4])
		#var = self.datalist[3] + (self.datalist[2]*255) + (self.datalist[1]*2*255) + (self.datalist[0]*2*2*255)
		#print var - 65535

		#if len(self.datalist) == 8:
		#	print self.datalist[0]

		#buffer = [chr((self.rpm >> 32) & 0xFF), chr((self.rpm >> 16) & 0xFF), chr((self.rpm >> 8) & 0xFF), chr((self.rpm) & 0xFF)]
		#id = 1
		#RPM = 3
		#key = id | ((RPM << 8) & 0xFFFFFFFF)

		#print buffer

		#self.setShared(str(key), string.join(buffer, ""))

		self.setDuty(self.rpm, 1)
		#self.setCurrent(self.rpm, 1);

		time.sleep(0.005)
		
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "drive_mode" in message:
			self.mode = message["drive_mode"]
		if "m1Stats" in message:
			(self.m1Count, self.m1Current, self.m1Temp, self.m1RPM) = struct.unpack(">ibbh", message["m1Stats"])
		if "axes" in message:
			#print message["axes"]
			#self.rpm = float(message["axes"][1])#int(self.expo(float(message["axes"][1])))
			#self.rpm =  self.expo(self.rpm)
			if self.mode == ControlMode.RPM:
				for i in range(0,3):
					self.setRPM(self.expo(message["axes"][0]), i)
				for i in range(3,6):
					self.setRPM(self.expo(message["axes"][1]), i)
			elif self.mode == ControlMode.CURRENT:
				for i in range(0,3):
					self.setCurrent(self.expo(message["axes"][0]), i)
				for i in range(3,6):
					self.setCurrent(self.expo(message["axes"][1]), i)
			elif self.mode == ControlMode.BRAKE:
				for i in range(0,3):
					self.setBrake(self.expo(message["axes"][0]), i)
				for i in range(3,6):
					self.setBrake(self.expo(message["axes"][1]), i)
				

	def cleanup(self):
		RoverProcess.cleanup(self)
		
