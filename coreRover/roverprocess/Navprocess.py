
from RoverProcess import RoverProcess
from libs.Piksi import Piksi

# your imports go here. For example:
import time
import socket
import serial

class NavProcess(RoverProcess):
	
	def getSubscribed(self):
		# Returns a dictionary of lists for all the incoming (self) and outgoing (server) subscriptions
		return {
				"self" : [],
				"json" : [],
				"can" : [],
				"web" : ["pos"]
				}

	def setup(self, args):
		# Navigation status
		#self.run = False;

		# UDP/Serial Link to SwiftNav Piksi Base software
		# From https://github.com/swift-nav/piksi_tools/blob/master/piksi_tools/ardupilot/udp_receive.py#L16
		#self.piksiAddr = "127.0.0.1"
		#self.piksiPort = 13320
		#self.piksiSerial = "/dev/ttyUSB0"
		#self.piksiBaud = 1000000

		#self.serLink = serial.Serial(self.piksiSerial, self.piksiBaud)
		#self.sockLink = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		#self.sockLink.bind(self.piksiAddr, self.piksiPort)
		
		# example: process = Navprocess(..., serial = ..., baud = ..., addr = ..., port = ...)
		self.piksi = Piksi(args["serial"], args["baud"], recv_addr=(args["addr"], args["port"]))
		try:
			self.piksi.start()
		except (EnvironmentError) as e:
            print "Error starting the piksi for navigation"

	def loop(self):
		# Getting UDP/Serial Link
		#data, addr = self.sockLink.recvfrom(1024)
		#if data:
		#	self.serLink.write(data)
		
		connected = self.piksi.connected()
		if not connected:
			print "Rover piksi is not receiving satelite observations"
		else:
			msg = self.piksi.poll(SBP_MSG_POS_LLH)
			if msg is not None:
				pos_msg = "lat" + str(msg.payload.lat) + "lon" + str(msg.payload.lon)
				self.setShared("pos", pos_msg)
		time.sleep(1)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		# your message handling here. for example:
		#if "exampleKey" in message:
		#	print "got: " + str(message["exampleKey"])


	def cleanup(self):
		self.piksi.stop()
		RoverProcess.cleanup(self)
		#if self.serLink.isopen():
		#	self.serLink.close()


	#-----------------------------------------------------------
	#navigation algorithm



	#-------------------------------------------------------------
	#functions to interact with the rest of the system


	#allows the rover to be controlled by software
	#needs to be called before any other nav function can be ran
	def startNav(self):
		global run = True



	#sets the motors to the giving values
	#pre: startNav has to already be called
	#left: the value for the left side motors
	#right: the value for the right side motor
	def move(self, left, right):
		if (run):
			#add code to map values between 0 to 1

			#send message to left side motors
			self.setShared("inputOneLeftY", str(left))
			#send message to right side motors
			self.setShared("inputOneRightY", str(right))
		else
			print "error: Navigation mode has not started"


	#ends software control for the rover
	#start Nav has to be called again
	def endNav(self):
		global run = False