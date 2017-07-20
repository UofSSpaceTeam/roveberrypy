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
from subprocess import call

class CameraProcess(RoverProcess):

	def setup(self, args):
		for key in ["start_cam_0", "start_cam_1", "stop_cam"]:
			self.subscribe(key)

	def on_start_cam_0(self, data):
		call("/home/pi/bin/start_video0.sh", shell=True)

	def on_start_cam_1(self, data):
		call("/home/pi/bin/start_video1.sh", shell=True)

	def on_stop_cam(self, data):
		call("killall mjpg_streamer", shell=True)
