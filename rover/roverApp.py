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

# test execution

print("starting")
startThreads()
print("running")

time.sleep(5)

print("stopping")
stopThreads()
print("done")

