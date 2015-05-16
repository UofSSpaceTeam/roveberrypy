import sys
sys.dont_write_bytecode = True
import os
import json

from threads.communicationThread import CommunicationThread
from threads.experimentThread import ExperimentThread
from threads.armThread import ArmThread
from threads.driveThread import DriveThread
from threads.telemetryThread import TelemetryThread
from threads.cameraThread import CameraThread
from threads.antennaCameraThread import AntennaCameraThread
from threading import Semaphore
import time

class RoverApp():
	def __init__(self):
		self.settings = json.loads(open("settings.json").read())
		self.i2cSemaphore = Semaphore(1)
		self.commThread = CommunicationThread(self, self.settings["port"])
		self.cameraThread = CameraThread(self)
		self.telemetryThread = TelemetryThread(self)
		self.driveThread = DriveThread(self, self.i2cSemaphore)
		self.armThread = ArmThread(self, self.i2cSemaphore)
		self.antennaCameraThread = AntennaCameraThread(self, self.i2cSemaphore)
		self.experimentThread = ExperimentThread(self, self.i2cSemaphore)

	def quit(self):
		os._exit(0)

	def startThreads(self):
		print("starting threads")
		self.commThread.start()
		self.cameraThread.start()
		#self.telemetryThread.start()
		self.driveThread.start()
		self.armThread.start()
		#self.antennaCameraThread.start()
		self.experimentThread.start()
	
	def run(self):
		self.startThreads()
		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			print("stopping")
			self.quit()
		except:
			self.quit()
			raise

RoverApp().run()

