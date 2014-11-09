import roverThreads
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
commThread = roverThreads.communicationThread()
cameraThread = roverThreads.cameraThread()
teleThread = roverThreads.telemetryThread()
driveThread = roverThreads.driveThread()
armThread = roverThreads.armThread()
experimentThread = roverThreads.experimentThread()

# configure threads
commThread.sendPort = 8000
commThread.receivePort = 8001
commThread.sendInterval = 0.1
commThread.cameraThread = cameraThread
commThread.teleThread = teleThread
commThread.driveThread = driveThread
commThread.armThread = armThread
commThread.experimentThread = experimentThread

# test execution

print("starting")
startThreads()
print("running")
time.sleep(1)

# test code goes here
commThread.inbox.put({"c1j1y":0.44})

time.sleep(1)
print("stopping")
stopThreads()
print("done")

