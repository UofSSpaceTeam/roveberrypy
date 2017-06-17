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
from roverprocess.arm17.arm import Joints, Controller, Config, ManualControl

# Any libraries you need can be imported here. You almost always need time!
import time
from multiprocessing.synchronize import BoundedSemaphore # BoundedSemaphore class used to block extra commands from conflicting with actual commands in operation.

base_max_speed = 40000
base_min_speed = 5000
shoulder_max_speed = 100000
shoulder_min_speed = 10100
elbow_max_speed = 100000
elbow_min_speed = 10100

dt = 1

class ArmProcess(RoverProcess):

	# Subscribe ArmProcess to joystick keys.
	def setup(self, args):
		for key in ["joystick1", "joystick2", "Rtrigger", "Ltrigger"]:
			self.subscribe(key)
		self.base_direction = None
		self.joints_pos = Joints(0, 0, 0, 0, 0, 0)
		self.speeds = Joints(0,0,0,0,0,0)
		self.command = [1,0,0,0,0,0]
		self.config = Config()
		self.controller = Controller(self.config)
		self.mode = ManualControl()


	def get_positions(self):
		''' Polls each VESC for their current possition.
			Currently just simulated values for testing.'''
		new_joints = list(self.joints_pos)
		for i in range(len(self.speeds)):
			if new_joints[i] is not None:
				new_joints[i] = self.joints_pos[i] + self.speeds[i] * dt
		return Joints(*tuple(new_joints))

	def loop(self):
		self.joints_pos = self.get_positions()
		self.controller.user_command(self.mode, *Joints(*self.command))
		self.speeds = self.controller.update_duties(self.joints_pos)
		self.log("joints_pos: {}".format(self.joints_pos))
		self.log("speeds: {}".format(self.speeds))
		time.sleep(dt)

	def on_joystick1(self, data):
		''' Shoulder joint'''
		y_axis = data[1]
		y_axis = (y_axis * shoulder_max_speed) # half power for testing
		if y_axis > shoulder_min_speed or y_axis < -shoulder_min_speed:
			armShoulderSpeed = int(y_axis)
		else:
			armShoulderSpeed = 0
		self.log("shoulder: " + str(armShoulderSpeed), "DEBUG")
		self.publish("wheelLB", SetDutyCycle(armShoulderSpeed))

	def on_joystick2(self, data): #y-axis vertical motion of elbow, x-axis joint along the length of the elbow
		''' Elbow joints.'''
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
		''' Base rotation right'''
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
		''' Base rotation left'''
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







