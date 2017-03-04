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
import pyvesc
from pyvesc import SetDutyCycle, SetRPM

# Any libraries you need can be imported here. You almost always need time!
import time
from multiprocessing.synchronize import BoundedSemaphore # BoundedSemaphore class used to block extra commands from conflicting with actual commands in operation.

base_max_speed = 40000
base_min_speed = 5000
shoulder_max_speed = 100000
shoulder_min_speed = 10100
elbow_max_speed = 100000
elbow_min_speed = 10100

class ArmProcess(RoverProcess):
    
	# Subscribe ArmProcess to joystick keys for multiprocessing.
	def setup(self, args):
		for key in ["joystick1", "joystick2", "Rtrigger", "Ltrigger"]: # Add the keys to the subscription of the multiprocessor.
			self.subscribe(key)
		self.base_direction = None
		self.shoulder_direction = None
		self.elbow_direction = None

	# Function that grabs the x and y axis values in message, then formats the data
	#  and prints the result to stdout.
	# Returns the newly formated x and y axis values in a new list

	def on_joystick1(self, data):
		y_axis = data[1]
		y_axis = (y_axis * shoulder_max_speed) # half power for testing
		if y_axis > shoulder_min_speed or y_axis < -shoulder_min_speed:
			armShoulderSpeed = int(y_axis)
		else:
			armShoulderSpeed = 0
		self.log("shoulder: " + str(armShoulderSpeed), "DEBUG")
		self.publish("wheelLB", SetDutyCycle(armShoulderSpeed))

	def on_joystick2(self, data): #y-axis vertical motion of elbow, x-axis joint along the length of the elbow
		y_axis = data[1]
		y_axis = (y_axis * elbow_max_speed/2)

		x_axis = data[0]
		x_axis = (x_axis * elbow_max_speed/2)

		if y_axis > elbow_min_speed or y_axis < -elbow_min_speed:
			armY_ElbowSpeed = int(y_axis)
		else:
			armY_ElbowSpeed = 0

		if x_axis > elbow_min_speed or x_axis < -elbow_min_speed:
			armX_ElbowSpeed = int(x_axis)
		else:
			armX_ElbowSpeed = 0

		self.log("elbow: " + str(armY_ElbowSpeed), "DEBUG")
		self.publish("wheelLF", SetDutyCycle(armY_ElbowSpeed))
		self.log(armX_ElbowSpeed, "DEBUG")
		self.publish("elbowX", SetDutyCycle(armX_ElbowSpeed))


	def on_Rtrigger(self, trigger):
		trigger = -1*(trigger + 1)/2
		armBaseSpeed = trigger * base_max_speed/2
		if self.base_direction is "right" or self.base_direction is None:
			if -base_min_speed <armBaseSpeed < base_min_speed:
				armBaseSpeed = 0
				self.base_direction = None
			else:
				self.base_direction = "right"
			self.log(armBaseSpeed, "DEBUG")
			self.publish("wheelLM", pyvesc.SetRPM(int(armBaseSpeed))) # Publish the process to the multiprocessor.


	def on_Ltrigger(self, trigger):
		trigger = (trigger + 1)/2
		armBaseSpeed = trigger * base_max_speed/2
		if self.base_direction is "left" or self.base_direction is None:
			if -base_min_speed <armBaseSpeed < base_min_speed:
				armBaseSpeed = 0
				self.base_direction = None
			else:
				self.base_direction = "left"
			self.log(armBaseSpeed, "DEBUG")
			self.publish("wheelLM", pyvesc.SetRPM(int(armBaseSpeed))) # Publish the process to the multiprocessor.







