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
from pyvesc import SetRPM
import pyvesc


class DriveProcess(RoverProcess):

	def setup(self, args):
		for key in ["joystick1", "joystick2", "on_DriveStop",
					"on_DriveForward", "on_DriveBackward",
					"on_DriveTurnRight", "on_DriveTurnLeft"]:
			self.subscribe(key)

	# Function that grabs the x and y axis values in message, then formats the data
	#  and prints the result to stdout.
	# Returns the newly formated x and y axis values in a new list
	def on_joystick1(self, data):
		y_axis = data[1]
		y_axis = (y_axis * 40000/2) # half power for testing
		if y_axis > 11000 or y_axis < -11000:
			newMessage = int(y_axis)
		else:
			newMessage = 0
		self.log(newMessage, "DEBUG")
		self.publish("wheelRF", SetRPM(newMessage))
		self.publish("wheelRM", SetRPM(newMessage))
		self.publish("wheelRB", SetRPM(newMessage))

	# Function that grabs the x and y axis values in message, then formats the data
	#  and prints the result to stdout.
	# Returns the newly formated x and y axis values in a new list
	def on_joystick2(self, data):
		y_axis = data[1]
		y_axis = (y_axis * 40000/2)
		if y_axis > 11000 or y_axis < -11000:
			newMessage = int(y_axis)
		else:
			newMessage = 0
		self.log(newMessage, "DEBUG")
		self.publish("wheelLF", SetRPM(newMessage))
		self.publish("wheelLM", SetRPM(newMessage))
		self.publish("wheelLB", SetRPM(newMessage))

	def _setLeftWheelSpeed(self, rpm):
		rpm = SetRPM(int(rpm))
		self.publish("wheelLF", rpm)
		self.publish("wheelLM", rpm)
		self.publish("wheelLB", rpm)

	def _setRightWheelSpeed(self, rpm):
		rpm = SetRPM(int(rpm))
		self.publish("wheelRF", rpm)
		self.publish("wheelRM", rpm)
		self.publish("wheelRB", rpm)

	def on_DriveStop(self, data):
		self._setLeftWheelSpeed(0)
		self._setRightWheelSpeed(0)

	def on_DriveForward(self, data):
		self._setLeftWheelSpeed(MOTOR_RPM)
		self._setRightWheelSpeed(MOTOR_RPM)

	def on_DriveBackward(self, data):
		self._setLeftWheelSpeed(-MOTOR_RPM)
		self._setRightWheelSpeed(-MOTOR_RPM)

	def on_DriveTurnRight(self, data):
		self._setLeftWheelSpeed(MOTOR_RPM)
		self._setRightWheelSpeed(-MOTOR_RPM)

	def on_DriveTurnLeft(self, data):
		self._setLeftWheelSpeed(-MOTOR_RPM)
		self._setRightWheelSpeed(MOTOR_RPM)









