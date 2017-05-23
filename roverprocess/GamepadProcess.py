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

from roverprocess import RoverProcess
from multiprocessing.synchronize import BoundedSemaphore
from pyvesc import SetRPM
import pyvesc

class GamepadProcess(RoverProcess):

    #Setup generic subscriptions for the joystick process.
    def setup(self, args):
        for key in ["joystick1", "joystick2", "Rtrigger", "Ltrigger"]:
            self.subscribe(key)

    # Function that grabs the x and y axis values in message, then formats the data
	#  and prints the result to stdout.
	# Returns the newly formated x and y axis values in a new list
    def on_joystick1(self, data):
        newMessage = self.createMessageJoystick1(data)
        self.publishMessageJoystick(newMessage)
        
    # Function that grabs the x and y axis values in message, then formats the data
	#  and prints the result to stdout.
	# Returns the newly formated x and y axis values in a new list
    def on_joystick2(self, data):
        newMessage = self.createMessageJoystick2(data)
        self.publishMessageJoysitck(newMessage)

    def on_Rtrigger(self, trigger):
        newMessage = self.createMessageTriggerR(trigger)
        self.publishMessageTrigger(newMessage)

    def on_Ltrigger(self, trigger):
        newMessage = self.createMessageTriggerL(trigger)
        self.publishMessageTrigger(newMessage)

    def publishMessageJoystick(self, message):
        None

    def publishMessageTrigger(self, message):
        None

    def createMessageJoystick1(self, input):
        None

    def createMessageJoystick2(self, input):
        None

    def createMessageTriggerL(self, input):
        None

    def createMessageTriggerR(self, input):
        None