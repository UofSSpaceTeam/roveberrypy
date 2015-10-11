import os, sys
sys.dont_write_bytecode = True
import time
import multiprocessing

# All modules ["Example", "JsonServer", "I2C"]
modulesList = []

# Check if on windows - if so do not run rover hardware specific code!
if(os.name == "nt"):
	modulesList = ["JsonServer", "Example", "WebServer"]
else:
	modulesList = ["JsonServer", "I2C"]

from StateManager import StateManager
if "JsonServer" in modulesList: from RoverProcess.JsonServer import JsonServer
if "Example" in modulesList: from RoverProcess.ExampleProcess import ExampleProcess
if "I2C" in modulesList: from RoverProcess.I2cExampleProcess import I2cExampleProcess
if "WebServer" in modulesList: from RoverProcess.WebserverProcess import WebserverProcess

# system configuration
localPort = 34567
remotePort = 34568

# build and run the system
if __name__ == "__main__":
	system = StateManager()
	processes = []
	i2cSem = multiprocessing.Semaphore(1)
	print "\nBUILD: Registering process subsribers...\n"

	if "JsonServer" in modulesList: 
		process = JsonServer(
			downlink = system.getDownlink(), uplink = system.getUplink(),
			local = localPort, remote = remotePort, sendPeriod = 0.1)
		system.addObserver("exampleTime", process.downlink)
		processes.append(process)
		
	if "Example" in modulesList:
		process = ExampleProcess(
			downlink = system.getDownlink(), uplink = system.getUplink())
		system.addObserver("exampleTime", process.downlink)
		processes.append(process)
		
	if "WebServer" in modulesList:
		process = WebserverProcess(
			downlink = system.getDownlink(), uplink = system.getUplink())
		processes.append(process)

	
	if "I2C" in modulesList:
		process = I2cExampleProcess(
			downlink = system.getDownlink(), uplink = system.getUplink(),
			sem = i2cSem)
		processes.append(process)
	
	# start everything
	print "\nSTARTING: " + str([type(p).__name__ for p in processes]) + "\n"
	for process in processes:
		process.start()

	# wait until ctrl-C or error
	try:
		while True:
			time.sleep(60)
	except KeyboardInterrupt:
		print("\nSTOP: " + str([type(p).__name__ for p in processes]) + "\n")		
	finally:
		system.terminateState()
