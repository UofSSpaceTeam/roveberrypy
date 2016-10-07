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


class Generator(RoverProcess):

	def getPublished(self):
		return ["generator"]

	def setup(self, args):
		self.text = "gg"

	def loop(self):
		print("gen running")
		self.setShared("generator", self.text)
		time.sleep(1)
