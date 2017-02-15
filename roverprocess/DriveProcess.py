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
from pyvesc import SetRPM, SetCurrent, SetCurrentBrake
import pyvesc

max_rpm = 40000
min_rpm = 10000
max_current = 4
min_current = 0.5

class DriveProcess(RoverProcess):

	def setup(self, args):
		self.right_brake = False
		self.left_brake = False
		self.drive_mode = "current"
		for key in ["joystick1", "joystick2", "Ltrigger", "Rtrigger"]:
			self.subscribe(key)

	# Function that grabs the x and y axis values in message, then formats the data
	#  and prints the result to stdout.
	# Returns the newly formated x and y axis values in a new list
	def on_joystick1(self, data):
		y_axis = data[1]
		if self.drive_mode == "rpm":
			speed = (y_axis * max_rpm/2) # half power for testing
			if -min_rpm < y_axis < min_rpm:
				speed = 0
			self.publish("wheel1", SetRPM(speed))
			self.publish("wheel2", SetRPM(speed))
			self.publish("wheel3", SetRPM(speed))
		elif self.drive_mode == "current" and not self.left_brake:
			current = (y_axis * max_current)
			if -min_current < current < min_current:
				current = 0
			self.publish("wheel1", SetCurrent(current))
			self.publish("wheel2", SetCurrent(current))
			self.publish("wheel3", SetCurrent(current))


	# Function that grabs the x and y axis values in message, then formats the data
	#  and prints the result to stdout.
	# Returns the newly formated x and y axis values in a new list
	def on_joystick2(self, data):
		y_axis = data[1]
		if self.drive_mode == "rpm":
			speed = (y_axis * max_rpm/2) # half power for testing
			if -min_rpm < y_axis < min_rpm:
				speed = 0
			self.publish("wheel4", SetRPM(speed))
			self.publish("wheel5", SetRPM(speed))
			self.publish("wheel6", SetRPM(speed))
		elif self.drive_mode == "current" and not self.right_brake:
			current = (y_axis * max_current)
			if -min_current < current < min_current:
				current = 0
			self.publish("wheel4", SetCurrent(current))
			self.publish("wheel5", SetCurrent(current))
			self.publish("wheel6", SetCurrent(current))

	def on_Ltrigger(self, trigger):
		if 0 < trigger <= 1 and self.drive_mode == "current":
			self.left_brake = True
			self.publish("wheel1", SetCurrentBrake(max_current))
			self.publish("wheel2", SetCurrentBrake(max_current))
			self.publish("wheel3", SetCurrentBrake(max_current))
		else:
			self.left_brake = False

	def on_Rtrigger(self, trigger):
		if 0 < message <= 1 and self.drive_mode == "current":
			self.right_brake = True
			self.publish("wheel4", SetCurrentBrake(max_current))
			self.publish("wheel5", SetCurrentBrake(max_current))
			self.publish("wheel6", SetCurrentBrake(max_current))
		else:
			self.right_brake = False











