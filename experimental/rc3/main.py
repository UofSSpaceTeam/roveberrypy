import sys, os
sys.dont_write_bytecode = True
import time
import multiprocessing

from statemanager import StateManager
from roverprocess import JsonServer

# system configuration
jsonPort = 37654
httpPort = 37680

def makeProcess(processType, **kwargs):
	assert type(processType) is RoverProcess
	processes.append(processType(
		system.getDownlinkQueue(), system.getUplinkQueue(), kwargs)

if __name__ == "__main__":
	# build and run the system
	system = StateManager()
	processes = []
	
	makeProcess(
	
	# start everything
	for proc in processes:
		proc.start()

	# wait until ctrl-C or error
	try:
		while True:
			time.sleep(60)
	except KeyboardInterrupt:
		print(
			"sending quit signal to " +
			str([type(p).__name__ for p in processes]))
	finally:
		system.terminate()
		os.remove("main.pyc")

