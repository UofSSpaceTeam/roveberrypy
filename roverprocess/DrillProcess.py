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
from pyvesc import SetDutyCycle
import pyvesc

import time
from multiprocessing.synchronize import BoundedSemaphore 

max_speed = 100000
min_speed = 10000


class DrillProcess(RoverProcess):

	def setup(self, args):
		for key in ["joystick1", "joystick2"]:
			self.subscribe(key)

	# Function that grabs the x and y axis values in message, then formats the data
	#  and prints the result to stdout.
	# Returns the newly formated x and y axis values in a new list
	def on_joystick1(self, data):
		y_axis = data[1]
		y_axis = (y_axis * max_speed) # half power for testing
		if y_axis > min_speed or y_axis < -min_speed:
			newMessage = int(y_axis)
		else:
			newMessage = 0

		self.log(newMessage, "DEBUG")
		self.publish("wheelLB", SetDutyCycle(newMessage))



	def on_joystick2(self, data):
		x_axis = data[0]
		x_axis = (x_axis * max_speed)
		if x_axis > min_speed or x_axis < -min_speed:
			duty = int(x_axis)
		else:
			duty = 0
		self.log("spin" + str(duty), "DEBUG")
		self.publish("wheelLF", SetDutyCycle(duty))

# add max/min speed parameters, as well as if spinning for button1