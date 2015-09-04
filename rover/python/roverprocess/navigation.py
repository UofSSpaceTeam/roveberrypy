from roverprocess import RoverProcess
from libs.sbp.pyserial_driver import PySerialDriver
from libs.sbp.handler import Handler
from libs.sbp.navigation import SBP_MSG_POS_LLH, MsgPosLLH
from libs.sbp.navigation import SBP_MSG_BASELINE_NED, MsgBaselineNED
from libs.sbp.settings import SBP_MSG_SETTINGS_WRITE, MsgSettingsWrite
import time
import serial
import math
import Queue as Q
import sys
#from nav_helpers import *

class Navigation(RoverProcess):
	'''GPS rover process
		contains a SBP handler for recieving and parsing sbp messages.
		Incomming messages:
			gps_posReq - request the current gps location
			gps_baselineReq - request the relative baseline position
		Outgoing messages:
			gps_Location - the current gps location
			gps_Baseline - the relative base position in NED coordinates.
		'''

	class NMEAPoint:
		 def __init__(self):
			self.lat = 0
			self.lng = 0
			self.hdg = 0
			self.hdop = 0

			

	def setup(self, args):
		import argparse
		parser = argparse.ArgumentParser(description="Swift Navigation SBP Example.")
		parser.add_argument("-p", "--port",
				default=['/dev/ttyUSB0'], nargs=1,
				help="specify the serial port to use.")
		args = parser.parse_args()

		# Open a connection to Piksi using the default baud rate (1Mbaud)
		self.driver = PySerialDriver(args.port[0], baud=1000000)
		self.handler = Handler(self.driver.read, self.driver.write, verbose=True)
		#self.handler.add_callback(self.pos_callback, msg_type=SBP_MSG_POS_LLH)
		# self.handler.add_callback(self.baseline_callback, msg_type=SBP_MSG_BASELINE_NED)
		#self.handler.start()
		self.magnetometer = serial.Serial(port="/dev/ttyAMA0", baudrate=9600, timeout=1)
		self.start = False # starts navigation when set to true 
		self.q = Q.PriorityQueue() # could be change to a normal queue
		self.command = None
		#load first few commands 
		#self.target = Coordinate(lat,lon)
		
		

	def loop(self):
		#if self.start is True: 
		#	self.runCommand()
		# self.getPos()
		p = self.readGPS_NMEA()
		print p.lat, p.lng
		self.setShared("NMEAlat", str(p.lat))
		self.setShared("NMEA_lng", p.lng)
		self.setShared("NMEA_hdg", p.hdg)
		self.setShared("NMEA_hdop", p.hdop)
		time.sleep(1)
		
	def readGPS_NMEA(self):
		p = self.NMEAPoint()
		rawData = self.driver.handle.read(self.driver.handle.inWaiting())
		dataStart = rawData.find("GGA")
		if dataStart != -1:	# found start of valid sentence
			dataEnd = min(dataStart + 70, len(rawData) - dataStart - 2)
			data = rawData[dataStart:dataEnd]
			values = data.split(",")
			if len(values) > 9:
				p.lat = float(values[2][:2])
				p.lat += float(values[2][2:])/60
				p.lng = float(values[4][:3])
				p.lng += float(values[4][3:])/60
				p.hdop = float(values[8])
				#altitude = float(values[9])
		return p

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
				#TODO: more descriptive error handling
		if "navHeartbeat" in message:
			self.setShared("navHeartbeat", True)
		if "gps_pos_lat" in message:
			try: self.setShared("latitude", self.getPos().lat)
			except: self.setShared("latitude", 0)
		if "gps_pos_lon" in message:
			try: self.setShared("longtitude", self.getPos().lon)
			except: self.setShared("longtitude", 0)
		if "gps_pos_height" in message:
			try: self.setShared("altitude", self.getPos().height)
			except: self.setShared("altitude", 0)
		if "gps_pos_flags" in message:
			self.setShared("gps_flags", self.getPos().flags)
		if "gps_baseline_n" in message:
			self.setShared("baseline_north", self.getBaseline().n)
		if "gps_baseline_e" in message:
			self.setShared("baseline_east", self.getBaseline().e)
		if "gps_baseline_d" in message:
			self.setShared("baseline_down", self.getBaseline().d)
		if "gps_baseline_flags" in message:
			self.setShared("baseline_flags", self.getBaseline().flags)
		if "compass_heading" in message:
			self.setShared("heading", self.getHeading())
		if "gps_heading" in message:
			try: self.setShared("heading", self.getGPSHeading())
			except: self.setShared("heading", 0)
			
		if "gps_NMEA" in message:
			print "NMEA Requested"
			


	def cleanup(self):
		try:
			self.handler.stop()
		except:
			pass
		RoverProcess.cleanup(self)

	# additional functions go here
	def getPos(self, timeout=5.0):
		''' Get current gps location
		timeout is in seconds
		'''
		
		try:
			p = MsgPosLLH(self.handler.wait(msg_type=SBP_MSG_POS_LLH, timeout=timeout))
			print p
			if not p == None:
				print "%.6f,%.6f,%.6f,%i" % (p.lat, p.lon, p.height, p.flags)
				return p
		except:
			return

	def getBaseline(self, timeout=5.0):
		''' Get relative baseline position in NED coordinates
		timeout is in seconds
		'''

		try:
			b = MsgBaselineNED(self.handler.wait(msg_type=SBP_MSG_BASELINE_NED, timeout=timeout))
			if not b == None:
				# print "%.4f, %.4f, %.4f, %i" % (b.n, b.e, b.d, b.flags)
				return b
		except Exception:
			print("Could not get baseline position")

	def setBaseLocation(self, p):
		''' Set the location of a surveyed base location
		p is an SBP_MSG_POS_LLH message containing the gps location of the base station
		'''
		self.handler.send_msg(MsgSettingsWrite(setting="[surveyed position, surveyed alt, {}]".format(p.height)))
		self.handler.send_msg(MsgSettingsWrite(setting="[surveyed position, surveyed lat, {}]".format(p.lat)))
		self.handler.send_msg(MsgSettingsWrite(setting="[surveyed position, surveyed lon, {}]".format(p.lon)))

	def getHeading(self):
		inchar = self.serial.read(1)
		if(inchar == "$"):
			#print "read complete", data
			return self.serial.readline()
		else:
			#print "no data, got: ", inchar
			return None

	def getGPSHeading(self):
		p1 = self.getBaseline()
		p2 = self.getBaseline()
		north = p2.n - p1.n
		east = p2.e - p1.e
		while math.hypot(east, north) < 200: #must move two centimeters (may need adjusting)
			p2 = self.getBaseline()
			north = p2.n - p1.n
			east = p2.e - p1.e
			time.sleep(0.5)
		heading = math.degrees(math.atan2(-1*east, north))
		if heading > 0:
			heading = 360 - heading
		else:
			heading = -1*heading
		return heading

	def runCommand(self):
		#an example on how to run the commands
		if self.command is not None:
			#self.command.update(self.getCoordinate())
			self.command.execute() 
			if self.command.isCancelled == True:
				self.command = None
		elif not self.q.empty():
			self.command = self.q.get()
			
	def addCommand(self, command):
		self.q.put(command)
	
	def removeAll(self):
		while not self.q.empty():
			self.q.get()
			
	# assuming we use the Coordinate class
	def getCoordinate(self):
		pass
		#return Coordinate(self.getPos().lat, self.getPos().lon, self.getHeading()) 
	
	def startNav(self):
		pass
		# loads the first few commands 
		#addCommand(TurnCommand(self.getCoordinate(), self.target))
		#addCommand(ForwardCommand(self.getCoordinate(), self.target))
