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
from roverprocess.arm17.arm import Joints, Controller, Config, ManualControl,Sections,Limits
from math import pi

# Any libraries you need can be imported here. You almost always need time!
import time

base_max_speed = 4
base_min_speed = 0.2
shoulder_max_speed = 4
shoulder_min_speed = 0.2
elbow_max_speed = 4
elbow_min_speed = 0.2

dt = 0.1

class ArmProcess(RoverProcess):

	def setup(self, args):
		for key in ["joystick1", "joystick2", "triggerR", "triggerL"]:
			self.subscribe(key)
		self.base_direction = None
		self.joints_pos = Joints(0, pi/4, 0, 0, 0, 0)
		self.speeds = Joints(0,0,0,0,0,0)
		self.command = [0,0,0,0,0,0]
		section_lengths = Sections(
				upper_arm=0.35,
				forearm=0.42,
				end_effector=0.1)
		joint_limits = Joints(
				# in radians
				base=None,
				shoulder=None,
				elbow=None,
				wrist_pitch=None,
				wrist_roll=None,
				gripper=None)
		max_angular_velocity = Joints(
				base=0.2,
				shoulder=0.2,
				elbow=0.2,
				wrist_pitch=0.2,
				wrist_roll=0.2,
				gripper=0.2)
		self.config = Config(section_lengths, joint_limits, max_angular_velocity)
		self.controller = Controller(self.config)
		self.mode = ManualControl()


	def get_positions(self):
		''' Polls each VESC for their current possition.
			Currently just simulated values for testing.'''
		new_joints = list(self.joints_pos)
		for i in range(len(self.speeds)):
			if new_joints[i] is not None:
				new_joints[i] = self.joints_pos[i] + self.speeds[i] * dt
		return Joints(*new_joints)

	def loop(self):
		self.joints_pos = self.get_positions()
		self.controller.user_command(self.mode, *Joints(*self.command))
		self.speeds = self.controller.update_duties(self.joints_pos)
		#publish speeds/duty cycles here
		self.log("joints_pos: {}".format(self.joints_pos))
		self.log("speeds: {}".format(self.speeds))
		self.publish("armShoulder", SetDutyCycle(int(100000*self.speeds[1])))
		self.publish("armElbow", SetDutyCycle(int(100000*self.speeds[2])))
		time.sleep(dt)

	def on_joystick1(self, data):
		''' Shoulder joint'''
		y_axis = data[1]
		y_axis = (y_axis * shoulder_max_speed)
		if y_axis > shoulder_min_speed or y_axis < -shoulder_min_speed:
			armShoulderSpeed = int(y_axis)
		else:
			armShoulderSpeed = 0
		self.command[1] = armShoulderSpeed

	def on_joystick2(self, data): #y-axis vertical motion of elbow, x-axis joint along the length of the elbow
		''' Elbow joints.'''
		y_axis = data[1]
		y_axis = (y_axis * elbow_max_speed)

		if y_axis > elbow_min_speed or y_axis < -elbow_min_speed:
			armY_ElbowSpeed = int(y_axis)
		else:
			armY_ElbowSpeed = 0
		self.command[2] = armY_ElbowSpeed

	def on_triggerR(self, trigger):
		''' Base rotation right'''
		trigger = -1*(trigger + 1)/2
		armBaseSpeed = trigger * base_max_speed/2
		if self.base_direction is "right" or self.base_direction is None:
			if -base_min_speed <armBaseSpeed < base_min_speed:
				armBaseSpeed = 0
				self.base_direction = None
			else:
				self.base_direction = "right"
			self.command[0] = armBaseSpeed


	def on_triggerL(self, trigger):
		''' Base rotation left'''
		trigger = (trigger + 1)/2
		armBaseSpeed = trigger * base_max_speed/2
		if self.base_direction is "left" or self.base_direction is None:
			if -base_min_speed <armBaseSpeed < base_min_speed:
				armBaseSpeed = 0
				self.base_direction = None
			else:
				self.base_direction = "left"
			self.command[0] = armBaseSpeed







