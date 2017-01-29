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

from .RoverProcess import RoverProcess

# Any libraries you need can be imported here. You almost always need time!
import time


class ArmProcess(RoverProcess):
	# Some blank space to write functions, classes, threads - whatever you need.
	# There are no restrictions - this is your own process!

	# See the tutorials on the wiki for things like basic threads and custom libraries.
	# < TO DO: INSTERT LINK TO THAT WIKI AND WRITE IT >

	# This is run once to set up anything you need.
	# Hint: use the self object to store variables global to this process.
	# You can also take any args you need from the main startup as a dictionary:
	# self.something = args["something"]
	# This can be handy for sharing semaphores with other processes!
    
    # Subscribe ArmProcess to joystick keys for multiprocessing.
    def setup(self, args):
        for key in ["joystick1", "joystick2"]: # Add the keys to the subscription of the multiprocessor.
            self.subscribe(key)

	# Function that grabs the x and y axis values in message, then formats the data
	#  and prints the result to stdout.
	# Returns the newly formated x and y axis values in a new list
    def on_joystick1(self, data):
        x_axis = data[0] # Get data for x-axis.
        x_axis = (x_axis * 40000/2) # Conversion factor to make it easy to interpret input.
        if x_axis > 11000 or x_axis < -11000: # If out of dead-zone.
            armBaseSpeed = x_axis
        else:
            armBaseSpeed = 0
        self.log(armBaseSpeed, "DEBUG") # Print the status of this process.
        self.publish("armBase", armBaseSpeed) # Publish the process to the multiprocessor.