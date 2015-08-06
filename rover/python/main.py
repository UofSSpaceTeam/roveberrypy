import sys
sys.dont_write_bytecode = True
import os
import time
import multiprocessing

from statemanager import StateManager
from roverprocess.jsonserver import JsonServer
from roverprocess.exampleprocess import ExampleProcess
from roverprocess.gps import GPS
from roverprocess.driveprocess import DriveProcess
# frim roverprocess.armprocess import ArmProcess

# system configuration
localPort = 34567
remotePort = 34568

# build and run the system
if __name__ == "__main__":
	system = StateManager()
	processes = []
	i2cSem = multiprocessing.Semaphore(1)
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
	
	# Piksi GPS process
	process = GPS(
		downlink = system.getDownlink(), uplink = system.getUplink())
	system.addObserver("gps_PosReq", process.downlink)
	system.addObserver("gps_BaselineReq", process.downlink)
	processes.append(process)
	
	# drive process
	process = DriveProcess(
		downlink = system.getDownlink(), uplink = system.getUplink(),
		sem = i2cSem)
	system.addObserver("inputOneLeftY", process.downlink)
	system.addObserver("inputOneRightY", process.downlink)
	processes.append(process)
	

	# arm process
	# process = ArmProcess(
	# 	downlink = system.getDownlink(), uplink = system.getUplink(),
	# 	sem = i2cSem)
	# system.addObserver("armAbsolute", process.downlink)
	# system.addObserver("armDirect", process.downlink)
	# system.addObserver("armThrottle", process.downlink)
	# processes.append(process)

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

