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

from .RoverServer import RoverServer

import time

class ExampleServer(RoverServer):

    def setup(self, args):
        #spawn 10 threads
        for i in list(range(0,10)):
            # spawnThread is inherited from RoverServer,
            # and takes a function, and any keyword arguments that the function needs.
            self.spawnThread(self.workerFunction, name=i)

    # This is a function specific to the ExampleServer class.
    # Takes in a variable number of keyword arguments.
    def workerFunction(self, **kwargs):
        while True:
            print("Testing server threading " + str(kwargs["name"]))
            time.sleep(2)

    # regular RoverProcess stuff
    def getSubscribed(self):
        return ["heartbeat"]
