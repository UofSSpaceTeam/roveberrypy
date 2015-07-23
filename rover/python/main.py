import sys
sys.dont_write_bytecode = True
import os
import time
import multiprocessing

from statemanager import StateManager
from roverprocess.jsonserver import JsonServer
from roverprocess.exampleprocess import ExampleProcess
from roverprocess.gps import GPS

# system configuration
localPort = 34567
remotePort = 34568

# build and run the system
if __name__ == "__main__":
	system = StateManager()
	processes = []
	print "\nBUILD\n"
	
	# json server
	process = JsonServer(
		downlink = system.getDownlink(), uplink = system.getUplink(),
		local = localPort, remote = remotePort, sendPeriod = 0.1)
	system.addObserver("exampleTime", process.downlink)
	processes.append(process)
	
	# example process
	process = ExampleProcess(
		downlink = system.getDownlink(), uplink = system.getUplink())
	system.addObserver("exampleKey", process.downlink)
	processes.append(process)
	
	process = GPS(
		downlink = system.getDownlink(), uplink = system.getUplink())
	system.addObserver("gpsMsg", process.downlink)
	processes.append(process)
	# start everything
	print "\nSTART: " + str([type(p).__name__ for p in processes]) + "\n"
	for process in processes:
		process.start()

	# wait until ctrl-C or error
	try:
		while True:
			time.sleep(60)
	except KeyboardInterrupt:
		print("\nSTOP: " + str([type(p).__name__ for p in processes]) + "\n")
	finally:
		system.terminate()
		os.remove("main.pyc")

