import sys
sys.dont_write_bytecode = True

#Import all of the thread modules
from threads.communicationThread import CommunicationThread
from threads.experimentThread import experimentThread
from threads.armThread import armThread
from threads.driveThread import driveThread
from threads.telemetryThread import telemetryThread
from threads.cameraThread import cameraThread
from threads.antenaCameraThread import antenaCameraThread

from threading import Semaphore
import time

i2cSemaphore = Semaphore(1)
class roverApp():
	def __init__(self):
		# make each top-level thread
		self.commThread = CommunicationThread(self, 35001)
		self.cameraThread = cameraThread(self)
		#self.telemetryThread = telemetryThread(self)
		self.driveThread = driveThread(self, i2cSemaphore)
		self.armThread = armThread(self,i2cSemaphore)
		self.antenaCameraThread = antenaCameraThread(self,i2cSemaphore)
		self.experimentThread = experimentThread(self, i2cSemaphore)


	def stopThreads(self):
		self.commThread.stop()
		self.cameraThread.stop()
		self.teleThread.stop()
		self.driveThread.stop()
		self.armThread.stop()
		self.antenaCameraThread.stop()
		experimentThread.stop()

	def startThreads(self):
		print("starting threads")
		self.commThread.start()
		self.cameraThread.start()
		#self.telemetryThread.start()
		self.driveThread.start()
		self.armThread.start()
		self.antenaCameraThread.start()
		self.experimentThread.start()
	
	def run(self):
		self.startThreads()
		# go until error
		try:
			while True:
				pass
		except KeyboardInterrupt:
			print("stopping")
			self.stopThreads()
		except:
			self.stopThreads()
			raise

app = roverApp()
app.run()
