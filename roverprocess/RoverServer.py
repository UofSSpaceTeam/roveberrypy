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

import time
import sys
from threading import Thread

class RoverServer(RoverProcess):

	class WorkerThread(Thread):
		def __init__(self, function, **kwargs):
			Thread.__init__(self)
			self.kwargs = kwargs
			self.function = function
			self.daemon = True

		def run(self):
			try:
				self.function(**self.kwargs)
			except KeyboardInterrupt:
				pass

	def __init__(self, **kwargs):
		RoverProcess.__init__(self, downlink=kwargs["downlink"],
				uplink=kwargs["uplink"])
		self.workers = []

	def spawnThread(self, function, **kwargs):
		new_thread = RoverServer.WorkerThread(function, **kwargs)
		self.workers.append(new_thread)
		new_thread.start()

	def cleanup(self):
		RoverProcess.cleanup(self)
		self.quit = True
		for thread in self.workers:
			try:
				thread.join(0.1)
			except KeyboardInterrupt:
				pass

