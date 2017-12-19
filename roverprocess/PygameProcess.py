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
import os
import pygame
from threading import Thread, BoundedSemaphore


class PygameProcess(RoverProcess):

	def setup(self, args):
		# so we can run in headless mode
		os.environ["SDL_VIDEODRIVER"] = "dummy"
		pygame.init()
		pygame.joystick.init()
		self.joystick1 = pygame.joystick.Joystick(0)
		self.joystick1.init()


	def loop(self):
		pygame.event.get()
		left = [self.joystick1.get_axis(0), self.joystick1.get_axis(1)]
		right = [self.joystick1.get_axis(3), self.joystick1.get_axis(4)]
		self.publish("joystick1", left)
		self.publish("joystick2", right)
		time.sleep(0.1)
