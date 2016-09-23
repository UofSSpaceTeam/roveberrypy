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
import inspect

# Check for hardware and load required modules
if(os.name == "nt"): # Windows test
	modulesList = []

elif(os.uname()[4] != "armv6l"): # Regular Linux/OSX test
	from signal import signal, SIGPIPE, SIG_DFL
	signal(SIGPIPE,SIG_DFL)
	modulesList = ["ExampleProcess"]

else: # Rover! :D
	print("Detected Rover hardware! Full config mode\n")
	from signal import signal, SIGPIPE, SIG_DFL
	signal(SIGPIPE,SIG_DFL)
	modulesList = []

print(modulesList)

# Import modules
from StateManager import StateManager
import importlib #for dynamic imports
import inspect

# dynamically import all modules in the modulesList
# try:
modules = [importlib.import_module("roverprocess."+name) for name in modulesList]
# except (ImportError):
#     print("Could not import modules") # CHANGE
#     sys.exit(1)

# module_classes is a list of lists where each list
# contains tuples for every class in the module, and each
# tuple contains a class name and a class object
module_classes = [inspect.getmembers(module, inspect.isclass) for module in modules]

# rover_classes is a list of classes to be instantiated.
rover_classes = []
for _list in module_classes:
    for tup in _list:
        if tup[0] in modulesList:
            rover_classes.append(tup[1])

print(rover_classes)

system = StateManager()
processes = []
for c in rover_classes:
    if c.__name__ in modulesList:
        instance = c(downlink=system.getDownlink(), uplink=system.getUplink())
        for sub in instance.getSubscribed()["self"]:
                system.addObserver(sub, instance.downlink)
        processes.append(instance)

# build and run the system
if __name__ == "__main__":


	print("\nBUILD: Registering process subsribers...\n")

	# start everything
	print("\nSTARTING: " + str([type(p).__name__ for p in processes]) + "\n")
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
