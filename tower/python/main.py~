import sys, os
sys.dont_write_bytecode = True
import time
import multiprocessing

from statemanager import StateManager
from roverprocess.jsonserver import JsonServer
from roverprocess.exampleprocess import ExampleProcess

# system configuration
jsonPort = 37654

# build and run the system
if __name__ == "__main__":
	system = StateManager()
	processes = []
	print "\nBUILD\n"
	
	# json server
	process = JsonServer(downlink = system.getDownlink(),
						uplink = system.getUplink(),
						port = jsonPort,
						sendPeriod = 0.1)
	system.addObserver("time", process.downlink)
	processes.append(process)
	
	# example process
	process = ExampleProcess(downlink = system.getDownlink(),
						uplink = system.getUplink())
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

