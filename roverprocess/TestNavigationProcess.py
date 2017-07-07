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
from roverprocess.GPSProcess import GPSPosition
import random

import time


class TestNavigationProcess(RoverProcess):
	

	def loop(self):
		for i in range(0,10):
			pos = GPSPosition(random.randrange(50,60),random.randrange(-120,-100))
			self.publish("wayPoint",pos)
		self.publish("saveWayPoint","E:\data.txt")
		time.sleep(5)
		self.publish("loadWayPoint","E:\data.txt")
		time.sleep(5)
		self.publish("clearWayPoint",True)


