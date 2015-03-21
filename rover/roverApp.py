import sys
sys.dont_write_bytecode = True

#Import all of the thread modules
from threads.communicationThread import communicationThread
from threads.experimentThread import experimentThread
from threads.armThread import armThread
from threads.driveThread import driveThread
from threads.telemetryThread import telemetryThread
from threads.cameraThread import cameraThread

import time

def stopThreads():
	commThread.stop()
	cameraThread.stop()
	#teleThread.stop()
	driveThread.stop()
	#armThread.stop()
	#experimentThread.stop()

# make each top-level thread
self.commThread = communicationThread(self, 31313)
self.cameraThread = cameraThread(self)
self.telemetryThread = telemetryThread(self)
self.driveThread = driveThread(self)
self.armThread = armThread(self)
self.experimentThread = experimentThread(self)

print("starting threads")
self.commThread.start()
self.cameraThread.start()
# self.telemetryThread.start()
self.driveThread.start()
# self.armThread.start()
# self.experimentThread.start()

# go until error
try:
	while True:
		pass
except:
	raise

print("stopping")
stopThreads()
