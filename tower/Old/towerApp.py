import sys
sys.dont_write_bytecode = True
import os

#Import all of the thread modules
from threads.communicationThread import CommunicationThread
from threads.motorThread import motorThread
from threads.telemetryThread import telemetryThread
from threads.cameraThread import CameraThread
import time

class towerApp():
	def __init__(self):
		# make each top-level thread
		self.commThread = CommunicationThread(self, 35001)
		self.telemetryThread = telemetryThread(self)
		self.motorThread = motorThread(self)
		self.cameraThread = CameraThread(self, 34567)

	def quit(self):
		os._exit(0)

	def startThreads(self):
		print("starting threads")
		self.commThread.start()
		self.telemetryThread.start()
		self.motorThread.start()
		self.cameraThread.start()
	
	def run(self):
		self.startThreads()
		try:
			while True:
				self.commThread.mailbox.put[("rotation":self.motorThread.getRotation)]
				time.sleep(1)
		except KeyboardInterrupt:
			print("stopping")
			self.quit()
		finally:
			self.quit()
			raise

towerApp().run()

