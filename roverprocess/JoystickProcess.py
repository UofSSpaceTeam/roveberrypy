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
from inputs import get_gamepad
from threading import Thread, BoundedSemaphore


class JoystickProcess(RoverProcess):

	class InputThread(Thread):
		def __init__(self, parent):
			Thread.__init__(self)
			self._parent = parent

		def run(self):
			while True:
				events = get_gamepad()
				with self._parent.joy_sem:
					for event in events:
						if event.code == "ABS_X":
							self._parent.joystick1[0] = event.state/32767
						elif event.code == "ABS_Y":
							self._parent.joystick1[1] = event.state/32767
						elif event.code == "ABS_RX":
							self._parent.joystick2[0] = event.state/32767
						elif event.code == "ABS_RY":
								self._parent.joystick2[1] = event.state/32767

	def setup(self, args):
		self.joystick1 = [0,0]
		self.joystick2 = [0,0]
		self.joy_sem = BoundedSemaphore(1)
		self.input_thread = JoystickProcess.InputThread(self)
		self.input_thread.start()

	def loop(self):
		with self.joy_sem:
			self.publish("joystick1", self.joystick1)
			self.publish("joystick2", self.joystick2)
		time.sleep(0.1)

	def cleanup(self):
		RoverProcess.cleanup(self)
		self.input_thread.join(1)


