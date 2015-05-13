import sys
sys.dont_write_bytecode = True
import os

#Import all of the thread modules
from threads.communicationThread import CommunicationThread
from threads.motorThread import motorThread
from threads.telemetryThread import telemetryThread
import time

class towerApp():
	def __init__(self):
		# make each top-level thread
		self.commThread = CommunicationThread(self, 35001)
		self.telemetryThread = telemetryThread(self)
		self.motorThread = motorThread(self)

	def quit(self):
		os._exit(0)

	def startThreads(self):
		print("starting threads")
		self.commThread.start()
		self.telemetryThread.start()
		self.motorThread.start()
	
	def run(self):
		self.startThreads()
		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			print("stopping")
			self.quit()
		finally:
			self.quit()
			raise

towerApp().run()

