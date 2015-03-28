import roverMessages
import threading
import json
from Queue import Queue
import time
from unicodeConvert import convert
#import serial 

class telemetryThread(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "telemetryThread"
		self.exit = False
		self.commThread = None
		self.mailbox = Queue()
		# set up serial, Serial(port, buadrate) 
		ser = serial.Serial("COM9", 115200)

		
	def run(self):
		while not self.exit:
			msg = {}
			# get info from sensor every 1 sec
			time.sleep(1)
			msg.update(self.sensorInfo())
			self.parent.commThread.mailbox.put(msg)
			
	# simulates receiving info from a sensor  		
	def sensorInfo(self):
		value = {}
		#add values to test
		#using c1j1y arbitrarily 
		#value["c1j1y"] = 0.5
		# read data from serial (USB)
		data = ser.read() 
		# TODO: parse data and send it through mailbox  
		
		
		
		
		return value 
		

	def stop(self):
		self.exit = True