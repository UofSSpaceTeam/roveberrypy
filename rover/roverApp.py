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

def startThreads():
	commThread.start()
	#cameraThread.start()
	#teleThread.start()
	driveThread.start()
	#armThread.start()
	#experimentThread.start()

def stopThreads():
	commThread.stop()
	#cameraThread.stop()
	#teleThread.stop()
	driveThread.stop()
	#armThread.stop()
	#experimentThread.stop()

# make each top-level thread
commThread = communicationThread()
cameraThread = cameraThread()
teleThread = telemetryThread()
driveThread = driveThread()
armThread = armThread()
experimentThread = experimentThread()

# configure threads
commThread.sendPort = 31313
commThread.receivePort = 31314
commThread.cameraThread = cameraThread
commThread.teleThread = teleThread
commThread.driveThread = driveThread
commThread.armThread = armThread
commThread.experimentThread = experimentThread

teleThread.commThread = commThread

print("starting")
startThreads()

# go until error
try:
	while True:
		pass
except:
	raise

print("stopping")
stopThreads()
