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

RPM_TO_ERPM = 12*19 # 12 poles, 19:1 gearbox

# Limits for Electronic RPM.
# Note this is not the RPM of the wheel, but the
# speed at which the motor is commutated.

deadzone = 0.1
max_rpm = 40000
min_rpm = 300
max_current = 6
min_current = 0.1
curve_val = 17

def rpm_curve(f):
	if f > 0:
		rpm = (1/5)*max_rpm + (4/5)*max_rpm*((expm1(2*f))/(expm1(4)))
	elif f < 0:
		f = -1*f
		rpm = (1/5)*max_rpm + (4/5)*max_rpm*((expm1(2*f))/(expm1(4)))
		rpm = -1*rpm
	else:
		rpm = 0

	#print(rpm)
	return rpm

def current_curve(f):
	if f > 0:
		current = (1/5)*max_current + (4/5)*max_current*((expm1(2*f))/(expm1(4)))
	elif f < 0:
		f = -1*f
		current = (1/5)*max_current + (4/5)*max_current*((expm1(2*f))/(expm1(4)))
		current = -1*current
	else:
		current = 0
	return current

def austin_rpm_curve(f):

	a = ((curve_val**abs(f)) - 1)/(curve_val - 1)
	
	if f > 0:
		#print(a*40000)
		return a*max_rpm
	else:
		#print(-a*40000)
		return -a*max_rpm

def austin_current_curve(f):
	
	a = ((curve_val**abs(f)) - 1)/(curve_val - 1)
	if f > 0:
		return a*max_current*100

	else:
		return -a*max_current*100

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
		for key in ["joystick1", "joystick2","triggerL","triggerR", "on_DriveStop",
					"on_DriveForward", "on_DriveBackward",
					"on_DriveRotateRight", "on_DriveRotateLeft", "buttonA_down"]:
			self.subscribe(key)

	def on_joystick1(self, data):
		""" Handles the left wheels for manual control.
			A joystick1 message contains:
			[x axis (float -1:1), y axis (float -1:1)]
		"""
		y_axis = data[1]
		if y_axis is None:
			return
		if self.drive_mode == "rpm":
			self.log("rpm")
			speed = austin_rpm_curve(y_axis)
			if -deadzone < y_axis < deadzone: # deadzone
				speed = 0
			self.publish("wheelLF", SetRPM(int(speed)))
			self.publish("wheelLM", SetRPM(int(-1*speed)))
			self.publish("wheelLB", SetRPM(int(speed)))
			self.publish("updateLeftWheelRPM", speed)
			self.log("left: {}".format(speed))
		elif self.drive_mode == "current" and not self.left_brake:
			current = austin_current_curve(y_axis)
			self.publish("wheelLF", SetCurrent(current))
			self.publish("wheelLM", SetCurrent(current))
			self.publish("wheelLB", SetCurrent(current))
			self.log(current)



	def on_joystick2(self, data):
		""" Handles the right wheels for manual control.
			A joystick1 message contains:
			[x axis (float -1:1), y axis (float -1:1)]
		"""
		y_axis = data[1]
		print(data)
		if y_axis is None:
			return
		if self.drive_mode == "rpm":
			speed = austin_rpm_curve(y_axis)
			if -deadzone < y_axis < deadzone: # deadzone
				speed = 0
			self.publish("wheelRF", SetRPM(int(speed)))
			self.publish("wheelRM", SetRPM(int(speed)))
			self.publish("wheelRB", SetRPM(int(-1*speed)))
			self.publish("updateRightWheelRPM", speed)
			self.log("right: {}".format(speed))
		elif self.drive_mode == "current" and not self.right_brake:
			current = austin_current_curve(y_axis)
			#if -min_current < current < min_current:
			#	current = 0
			self.publish("wheelRF", SetCurrent(current))
			self.publish("wheelRM", SetCurrent(current))
			self.publish("wheelRB", SetCurrent(current))
			self.log(current)
		# Single drive mode not working due to missing axis on Windows
		#if self.drive_mode == "single":
		#	speed = rpm_curve(y_axis)
		#	if -deadzone < y_axis < deadzone: # deadzone
		#		speed = 0
		#	self.publish("wheelRF", SetRPM(int( 1*(speed + self.mix))))
		#	self.publish("wheelRM", SetRPM(int( 1*(speed + self.mix))))
		#	self.publish("wheelRB", SetRPM(int(-1*(speed + self.mix))))
		#	self.publish("wheelLF", SetRPM(int( 1*(speed - self.mix))))
		#	self.publish("wheelLM", SetRPM(int(-1*(speed - self.mix))))
		#	self.publish("wheelLB", SetRPM(int( 1*(speed - self.mix))))
		#	#self.log("right: {}".format(speed))

	def on_Ltrigger(self, trigger):
		""" Handles left wheel braking (requires current mode)"""
		if 0 < trigger <= 1 and self.drive_mode == "current":
			self.left_brake = True
			self.publish("wheel1", SetCurrentBrake(max_current))
			self.publish("wheel2", SetCurrentBrake(max_current))
			self.publish("wheel3", SetCurrentBrake(max_current))
		else:
			self.left_brake = False

	def on_Rtrigger(self, trigger):
		""" Handles right wheel braking (requires current mode)"""
		if 0 < trigger <= 1 and self.drive_mode == "current":
			self.right_brake = True
			self.publish("wheel4", SetCurrentBrake(max_current))
			self.publish("wheel5", SetCurrentBrake(max_current))
			self.publish("wheel6", SetCurrentBrake(max_current))
		else:
			self.right_brake = False

	def on_ButtonA_down(self, val):
		self.publish("autoDrive")

	def on_ButtonB_down(self, val):
		self.publish("manualDrive")

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

	def on_DriveForward(self, speed):
		self._setLeftWheelSpeed(speed*RPM_TO_ERPM)
		self._setRightWheelSpeed(speed*RPM_TO_ERPM)

	def on_DriveBackward(self, speed):
		self._setLeftWheelSpeed(-speed*RPM_TO_ERPM)
		self._setRightWheelSpeed(-speed*RPM_TO_ERPM)

	def on_DriveRotateRight(self, speed):
		self._setLeftWheelSpeed(speed*RPM_TO_ERPM)
		self._setRightWheelSpeed(-speed*RPM_TO_ERPM)

	def on_DriveRotateLeft(self, speed):
		self._setLeftWheelSpeed(-speed*RPM_TO_ERPM)
		self._setRightWheelSpeed(speed*RPM_TO_ERPM)









