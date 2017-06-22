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
from math import expm1, exp
import time
from multiprocessing.synchronize import BoundedSemaphore 

max_speed = 100000
min_speed = 10000
drill_speed = 50000 #don't know the actual value

curve_val = 5

def rpm_curve(f):
	a = ((curve_val**abs(f)) - 1)/(curve_val - 1)
	if f > 0:
		return a*max_rpm
	else:
		return -a*max_rpm	

class DrillProcess(RoverProcess):

	def setup(self, args):
		self.drill_mode = False
		for key in ["joystick1", "bumperR"]:
			self.subscribe(key)

	# Function that grabs the x and y axis values in message, then formats the data
	#  and prints the result to stdout.
	# Returns the newly formated x and y axis values in a new list
	def on_joystick1(self, data):
		y_axis = data[1]
		if y_axis is None:
			return
		if self.drill_mode = True:
			self.log("drill on")
			speed = rpm_curve(y_axis)
			if -min_rpm < speed < min_rpm: #deadzone
				speed = 0
			self.publish("drillVertical", SetDutyCycle(int(speed)))
			self.log("drillVertical: {}".format(speed))

	def on_bumperR(self, data):
		if bumper is None:
			return
		if 0 < bumper <= 1 and self.drill_mode == False:
			self.drill_mode = True
			self.publish("drillRotate", SetDutyCycle(drill_speed))
		else:
			self.drill_mode == False

# add max/min speed parameters, as well as if spinning for button1