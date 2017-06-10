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
from math import expm1 # e**x - 1  for rpm/current curves
from math import exp

max_rpm = 40000
min_rpm = 2000
max_current = 0.5
min_current = 0.1
curve_val = 5

def rpm_curve(f):
	a = ((curve_val**abs(f)) - 1)/(curve_val - 1)
	if f > 0:
		return a*max_rpm
	else:
		return -a*max_rpm

def current_curve(f):
	a = ((curve_val**abs(f)) - 1)/(curve_val - 1)
	if f > 0:
		return a*max_current
	else:
		return -a*max_current

class DriveProcess(RoverProcess):
	"""Handles driving the rover.

	Takes joystick input from the web ui and
	commands the wheels to move. Uses RPM and current control modes.
	"""

	def setup(self, args):
		""" Initialize drive mode (default=rpm)."""
		self.right_brake = False
		self.left_brake = False
		self.drive_mode = "rpm"
		for key in ["joystick1", "joystick2", "triggerL", "triggerR"]:
			self.subscribe(key)

	def on_joystick1(self, data):
		""" Handles the left wheels for manual control. """
		y_axis = data[1]
		if y_axis is None:
			return
		if self.drive_mode == "rpm":
			self.log("rpm")
			speed = rpm_curve(y_axis)
			if -min_rpm < speed < min_rpm: # deadzone
				speed = 0
			self.publish("wheelLF", SetRPM(int(speed)))
			self.publish("wheelLM", SetRPM(int(speed)))
			self.publish("wheelLB", SetRPM(int(speed)))
			self.log("left: {}".format(speed))
		elif self.drive_mode == "current" and not self.left_brake:
			current = current_curve(y_axis)
			if -min_current < current < min_current:
				current = 0
			self.publish("wheelLF", SetCurrent(current))
			self.publish("wheelLM", SetCurrent(current))
			self.publish("wheelLB", SetCurrent(current))
			self.log("left: {}".format(current))


	def on_joystick2(self, data):
		""" Handles the right wheels for manual control. """
		y_axis = data[0]
		if y_axis is None:
			return
		if self.drive_mode == "rpm":
			speed = rpm_curve(y_axis)
			if -min_rpm < speed < min_rpm: # deadzone
				speed = 0
			self.publish("wheelRF", SetRPM(int(speed)))
			self.publish("wheelRM", SetRPM(int(speed)))
			self.publish("wheelRB", SetRPM(int(speed)))
			self.log("right: {}".format(speed))
		elif self.drive_mode == "current" and not self.right_brake:
			current = current_curve(y_axis)
			if -min_current < current < min_current:
				current = 0
			self.publish("wheelRF", SetCurrent(current))
			self.publish("wheelRM", SetCurrent(current))
			self.publish("wheelRB", SetCurrent(current))
			self.log("right: {}".format(current))

	def on_triggerL(self, trigger):
		""" Handles left wheel braking (requires current mode)"""
		if trigger is None:
			return
		if 0 < trigger <= 1 and self.drive_mode == "current":
			self.left_brake = True
			self.publish("wheel1", SetCurrentBrake(trigger*max_current))
			self.publish("wheel2", SetCurrentBrake(trigger*max_current))
			self.publish("wheel3", SetCurrentBrake(trigger*max_current))
		else:
			self.left_brake = False

	def on_triggerR(self, trigger):
		""" Handles right wheel braking (requires current mode)"""
		if trigger is None:
			return
		if 0 < trigger <= 1 and self.drive_mode == "current":
			self.right_brake = True
			self.publish("wheel4", SetCurrentBrake(trigger*max_current))
			self.publish("wheel5", SetCurrentBrake(trigger*max_current))
			self.publish("wheel6", SetCurrentBrake(trigger*max_current))
		else:
			self.right_brake = False











