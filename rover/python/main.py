import os
import time
import multiprocessing

# All modules ["Example", "JsonServer"]
modulesList = ["JsonServer", "Example"]

from statemanager import StateManager
if "JsonServer" in modulesList: from roverprocess.jsonserver import JsonServer
if "Example" in modulesList: from roverprocess.exampleprocess import ExampleProcess

# system configuration
localPort = 34567
remotePort = 34568

# build and run the system
if __name__ == "__main__":
	system = StateManager()
	processes = []
	i2cSem = multiprocessing.Semaphore(1)
	print "\nBUILD\n"

	if "JsonServer" in modulesList: 
		process = JsonServer(
			downlink = system.getDownlink(), uplink = system.getUplink(),
			local = localPort, remote = remotePort, sendPeriod = 0.1)
		system.addObserver("exampleTime", process.downlink)
		processes.append(process)
		
	if "Example" in modulesList:
		process = ExampleProcess(
			downlink = system.getDownlink(), uplink = system.getUplink())
		system.addObserver("ExampleTime", process.downlink)
		processes.append(process)
		
	# start everything
	print "\nSTART: " + str([type(p).__name__ for p in processes]) + "\n"
	for process in processes:
		process.start()

	# wait until ctrl-C or error
	# Note: There is a bug here and sometimes the software fails to exit cleanly
	try:
		while True:
			time.sleep(60)
	except KeyboardInterrupt:
		print("\nSTOP: " + str([type(p).__name__ for p in processes]) + "\n")
	finally:
		system.terminate()