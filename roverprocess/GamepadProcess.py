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
from multiprocessing.synchronize import BoundedSemaphore
from pyvesc import SetRPM
import pyvesc

class GamepadProcess(RoverProcess):

    # Setup generic subscriptions for the gamepad processes.
    # If you are extendimg this class and overwriting this function,
    # make sure you call GamepadProcess.setup(self) in the setup of the extended class
    # (similar as to overwriting RoverProcess.cleanup()).
    def setup(self, args):
        for key in ["joystick1", "joystick2", "Rtrigger", "Ltrigger"]:
            self.subscribe(key)

    # Function that grabs the x and y axis values in message, then formats the data
	#  and prints the result to stdout.
	# Returns the newly formated x and y axis values in a new list
    def on_joystick1(self, data):
        raise NotImplementedError
        
    # Function that grabs the x and y axis values in message, then formats the data
	#  and prints the result to stdout.
	# Returns the newly formated x and y axis values in a new list
    def on_joystick2(self, data):
        raise NotImplementedError

    def on_Rtrigger(self, trigger):
        raise NotImplementedError

    def on_Ltrigger(self, trigger):
        raise NotImplementedError