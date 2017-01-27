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

import os
import sys
sys.dont_write_bytecode = True #prevent generation of .pyc files on imports
import time
import logging
import inspect # for dynamic imports
import importlib #for dynamic imports
from StateManager import StateManager

logging.basicConfig(filename = 'main.log', filemode = 'w', level = logging.DEBUG) #creates new log each time it's run

# Check for hardware and load required modules
# Add the class name of a module to modulesLis to enable it
if(os.name == "nt"): # Windows test
	modulesList = []

elif(os.uname()[4] != "armv6l"): # Regular Linux/OSX test
	from signal import signal, SIGPIPE, SIG_DFL
	signal(SIGPIPE, SIG_DFL)
	modulesList = ["ExampleProcess", "USBServer", "DriveProcess", "WebServer"]

else: # Rover! :D
	print("Detected Rover hardware! Full config mode\n")
	logging.info("Rover hardware detected. Full config mode") 
	from signal import signal, SIGPIPE, SIG_DFL
	signal(SIGPIPE, SIG_DFL)
	modulesList = []

print("Enabled modules:")
print(modulesList)
logging.info("Enabled modules:")
logging.info(modulesList)


# Dynamically import all modules in the modulesList
modules = []
for name in modulesList:
	try:
		modules.append(importlib.import_module("roverprocess." + name))
	except (ImportError):
		print("\nERROR: Could not import " + name)
		logging.error("Could not import " + name)
		raise

# module_classes is a list of lists where each list
# contains tuples for every class in the module, and each
# tuple contains a class name and a class object
module_classes = [inspect.getmembers(module, inspect.isclass) for module in modules]

# rover_classes is a list of classes to be instantiated.
rover_classes = []
for _list in module_classes:
	for _tuple in _list:
		if _tuple[0] in modulesList:
			rover_classes.append(_tuple[1])


# build and run the system
if __name__ == "__main__":

	system = StateManager()
	processes = []
	print("\nBUILD: Registering process subsribers...\n")
	logging.info("Registering process subscribers...")
	for _class in rover_classes:
		# if _class was enabled, instantiate it,
		# and hook it up to the messaging system
		if _class.__name__ in modulesList:
			instance = _class(manager=system)
			for msg_key in instance.getSubscribed():
				system.addSubscriber(msg_key, instance)
			processes.append(instance)

	# start everything
	print("\nSTARTING: " + str([type(p).__name__ for p in processes]) + "\n")
	logging.info("STARTING: " + str([type(p).__name__ for p in processes]) )
	
	for process in processes:
		process.start()

	# wait until ctrl-C or error
	try:
		while True:
			time.sleep(60)
	except KeyboardInterrupt:
		print("\nSTOP: " + str([type(p).__name__ for p in processes]) + "\n")
		logging.info("STOP: " + str([type(p).__name__ for p in processes]) )
	finally:
		system.terminateState()
