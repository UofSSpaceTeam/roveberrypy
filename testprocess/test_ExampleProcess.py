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

from roverprocess.RoverProcess import RoverProcess

import time


class test_ExampleProcess(RoverProcess):
	def getSubscribed(self):
		return ["response"]

	def setup(self, args):
		self.num_out = 0
		self.num_in = 0;

	def loop(self):
		while self.num_in != self.num_out:
			time.sleep(0.05) # hacky way to syncronize with other process
		#send a test message. subscribers sould return false
		self.publish("respondTrue", False)
		self.num_out += 1
		time.sleep(1)

	def on_response(self, data):
		self.num_in += 1
		if data:
			self.log("Got response", "DEBUG")
		else:
			self.log("Receiver did not respond correctly", "ERROR")


