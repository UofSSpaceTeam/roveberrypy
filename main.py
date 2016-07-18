# Copyright 2016 University of Saskatchewan Space Design Team Licensed under the
# Educational Community License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may
# obtain a copy of the License at
#
# https://opensource.org/licenses/ecl2.php
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing
# permissions and limitations under the License.

import os, sys
sys.dont_write_bytecode = True
import time
import multiprocessing

# Check for hardware and load required modules
if(os.name == "nt"): # Windows test
	modulesList = []

elif(os.uname()[4] != "armv6l"): # Regular Linux/OSX test
	from signal import signal, SIGPIPE, SIG_DFL
	signal(SIGPIPE,SIG_DFL)
	modulesList = []

else: # Rover! :D
	print "Detected Rover hardware! Full config mode\n"
	modulesList = []
	from signal import signal, SIGPIPE, SIG_DFL
	signal(SIGPIPE,SIG_DFL)

print modulesList

# Import modules
from StateManager import StateManager
if "JsonServer" in modulesList: from roverprocess.JsonServer import JsonServer
if "Example" in modulesList: from roverprocess.ExampleProcess import ExampleProcess
if "WebServer" in modulesList: from roverprocess.WebServer import WebServer
if "CanServer" in modulesList: from roverprocess.CanServer import CanServer

# system configuration
localPort = 34567
remotePort = 34568

# build and run the system
if __name__ == "__main__":
	system = StateManager()
	processes = []
	jsonSubs = []
	canSubs = []
	webSubs = []

	i2cSem = multiprocessing.Semaphore(1)

	# macro for configuring threads
	def subDelegate(module):
		for sub in module.getSubscribed()["self"]:
			system.addObserver(sub, module.downlink)
		jsonSubs.extend(module.getSubscribed()["json"])
		canSubs.extend(module.getSubscribed()["can"])
		webSubs.extend(module.getSubscribed()["web"])
		processes.append(module)

	print "\nBUILD: Registering process subsribers...\n"

	# modules
	if "Example" in modulesList:
		process = ExampleProcess(
			downlink = system.getDownlink(), uplink = system.getUplink())
		subDelegate(process)

	# servers
	if "CanServer" in modulesList:
		process = CanServer(
			downlink = system.getDownlink(), uplink=system.getUplink(), sendPeriod = 0.01)
		for sub in canSubs:
			system.addObserver(sub, process.downlink)
		processes.append(process)

	if "JsonServer" in modulesList:
		process = JsonServer(
			downlink = system.getDownlink(), uplink = system.getUplink(),
			local = localPort, remote = remotePort, sendPeriod = 0.1)
		for sub in jsonSubs:
			system.addObserver(sub, process.downlink)
		processes.append(process)

	if "WebServer" in modulesList:
		process = WebServer(
			downlink = system.getDownlink(), uplink = system.getUplink())
		for sub in webSubs:
			print sub
			system.addObserver(sub, process.downlink)
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
