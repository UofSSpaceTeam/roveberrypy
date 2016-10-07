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

# Any libraries you need can be imported here. You almost always need time!
import time


class Receiver2(RoverProcess):

	def setup(self, args):
		self.someVariable = 42

	def loop(self):
		print("receiver2 running")
		time.sleep(2)
		self.subscribe("generator")

	# This runs every time a new message comes in.
	#	It is often handy to have an if statement for every type of message you expect
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)

		if "generator" in message:
			print("Receiver2 got: " + str(message["generator"]))
