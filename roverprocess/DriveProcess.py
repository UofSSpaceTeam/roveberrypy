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


class DriveProcess(RoverProcess):

    # Subscribed to joystick1 and joystick2.
	def getSubscribed(self):
		return ["joystick1", "joystick2"]

	# Function that grabs the x and y axis values in message, then formats the data
	#  and prints the result to stdout.
	# Returns the newly formated x and y axis values in a new list
	def on_joystick1(self, message):
		x_axis = message[0]
		y_axis = message[1]
		x_axis = (x_axis * 255)
		y_axis = (y_axis * 255)
		newMessage = [x_axis, y_axis]
		#print(newMessage)
		self.publish("wheel1", newMessage)
		self.publish("wheel2", newMessage)
		self.publish("wheel3", newMessage)


	# Function that grabs the x and y axis values in message, then formats the data
	#  and prints the result to stdout.
	# Returns the newly formated x and y axis values in a new list
	def on_joystick2(self, message):
		x_axis = message[0]
		y_axis = message[1]
		x_axis = (x_axis * 255)
		y_axis = (y_axis * 255)
		newMessage = [x_axis, y_axis]
		#print(newMessage)
		self.publish("wheel4", newMessage)
		self.publish("wheel5", newMessage)
		self.publish("wheel6", newMessage)











