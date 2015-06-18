import sys, os
sys.dont_write_bytecode = True
import time
import multiprocessing

from statemanager import StateManager
from jsonserver import JsonServer
from roverprocess import RoverProcess

if __name__ == "__main__":
	# build and run the system
	system = StateManager()
	processes = []

	toServer = system.getDownlinkQueue()
	fromServer = system.getUplinkQueue()
	proc = JsonServer(37654, toServer, fromServer)
	processes.append(proc)
	proc.start()

	upQ = system.getUplinkQueue()
	downQ = system.getDownlinkQueue()
	proc = RoverProcess(upQ, downQ)
	processes.append(proc)
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

