#Import all of the thread modules
from threads.communicationThread import communicationThread
from threads.guiThread import guiThread
from threads.inputThread import inputThread
from threads.navigationThread import navigationThread
from threads.panelThread import panelThread

import time

def startThreads():
	commThread.start()
	inputThread.start()
	navThread.start()
	panelThread.start()
	guiThread.start()

def stopThreads():
	commThread.stop()
	inputThread.stop()
	navThread.stop()
	panelThread.stop()
	guiThread.stop()


# make each top-level thread
commThread = communicationThread()
inputThread = inputThread()
navThread = navigationThread()
panelThread = panelThread()
guiThread = guiThread()

# configure threads
commThread.sendPort = 8001
commThread.receivePort = 8000
commThread.sendInterval = 0.25
commThread.inputThread = inputThread
commThread.navThread = navThread
commThread.panelThread = panelThread
commThread.guiThread = guiThread

inputThread.commThread = commThread

# test execution
print("starting")
startThreads()
print("running")
time.sleep(2)

# test code goes here

time.sleep(20)
print("stopping")
stopThreads()
print("done")

