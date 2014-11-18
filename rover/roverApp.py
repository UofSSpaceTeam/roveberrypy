#Import all of the thread modules
from communicationThread import communicationThread
from experimentThread import experimentThread
from armThread import armThread
from driveThread import driveThread
from telemetryThread import telemetryThread
from cameraThread import cameraThread

import time

def startThreads():
	commThread.start()
	cameraThread.start()
	teleThread.start()
	driveThread.start()
	armThread.start()
	experimentThread.start()

def stopThreads():
	commThread.stop()
	cameraThread.stop()
	teleThread.stop()
	driveThread.stop()
	armThread.stop()
	experimentThread.stop()


# make each top-level thread
commThread = communicationThread()
cameraThread = cameraThread()
teleThread = telemetryThread()
driveThread = driveThread()
armThread = armThread()
experimentThread = experimentThread()

# configure threads
commThread.sendPort = 8000
commThread.receivePort = 8001
commThread.sendInterval = 0.25
commThread.cameraThread = cameraThread
commThread.teleThread = teleThread
commThread.driveThread = driveThread
commThread.armThread = armThread
commThread.experimentThread = experimentThread

# test execution
print("starting")
startThreads()
print("running")
time.sleep(2)

# test code goes here
commThread.inbox.put({"c1j1y":0.44})

time.sleep(2)
print("stopping")
stopThreads()
print("done")

