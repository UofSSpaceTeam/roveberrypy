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
# from pyvesc import SetRPM
import pyvesc

class SensorProcess(RoverProcess):

    # This function sets up subscriptions, constants, etc. for the class.
    def setup(self, args):
        raise NotImplementedError

    # This is the function where all the sensor operations go.
    def loop(self):
        raise NotImplementedError