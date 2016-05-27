
from RoverProcess import RoverProcess
from libs.Piksi import Piksi
from libs.sbp.navigation import *
from libs.sbp.system import *
from libs.sbp.observation import *

# your imports go here. For example:
from threading import Thread
import time
import socket
import serial
import random

class NavProcess(RoverProcess):

	class PiksiThread(Thread):
		def __init__(self, parent, serial, baud, addr = None, port = None):
			Thread.__init__(self)
			
			self.parent = parent
			self.serial = serial
			self.baud = baud
			if addr is not None:
				self.addr = addr
				self.port = port
			
		def run(self):
			with Piksi(self.serial, self.baud, recv_addr=(self.addr, self.port)) as self.piksi:
				while True:
					connected = self.piksi.connected()
					if not connected:
						print "Rover piksi is not receiving satelite observations"
					else:
						print "Rover piksi is working"
						msg = self.piksi.poll(0x0201)
						if msg is not None:
							print "location"
							pos_msg = "lat:" + str(msg.lat) + ",lon:" + str(msg.lon)
							print pos_msg
							self.parent.setShared("pos", pos_msg)
						
					time.sleep(1)
	
	def getSubscribed(self):
		# Returns a dictionary of lists for all the incoming (self) and outgoing (server) subscriptions
		return {
				"self" : [],
				"json" : [],
				"can" : [],
				"web" : ["pos", "random_pos"]
				}

	def setup(self, args):
		
			
		receiver = NavProcess.PiksiThread(self, args["serial"], args["baud"], args["addr"], args["port"])	
		receiver.daemon = True
		receiver.start()

	def loop(self):
		
		pos_msg = "lat:" + str(random.uniform(-90, 90))+",lon:"+str(random.uniform(-180, 180))
		#print "no massage received"
		#print pos_msg
		self.setShared("random_pos", pos_msg)		
		time.sleep(1)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		

	def cleanup(self):
		
		RoverProcess.cleanup(self)
