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

    def __init__(self, **kwargs):
        RoverProcess.__init__(self, kwargs)
        
    # This function sets up subscriptions, constants, etc. for this class.
    # You do not need to call this method in a class that extends this one since sensors publish their own subscriptions
    # and use their own constants.
    # 
    # THROWS: NotImplementedError exception, thus it is highly recommended to use a TRY-EXCEPT
    # block (Python's TRY-CATCH block) when using this method.
    def setup(self, args):
        """
        This function sets up subscriptions, constants, etc. for this class.
        You do not need to call this method in a class that extends this one since sensors publish their own subscriptions
        and use their own constants.

        THROWS: NotImplementedError exception, thus it is highly recommended to use a TRY-EXCEPT
        block (Python's TRY-CATCH block) when using this method.
        """
        raise NotImplementedError

    # This is the function where all the sensor operations go.
    # This method should be implemented with another itentical function in a class that extends this one.
    # This will then allow for polymorphism.
    # 
    # THROWS: NotImplementedError exception, thus it is highly recommended to use a TRY-EXCEPT
    # block (Python's TRY-CATCH block) when using this method.
    def loop(self):
        """
        This is the function where all the sensor operations go.
        This method should be implemented with another itentical function in a class that extends this one.
        This will then allow for polymorphism.

        THROWS: NotImplementedError exception, thus it is highly recommended to use a TRY-EXCEPT
        block (Python's TRY-CATCH block) when using this method.
        """
        raise NotImplementedError