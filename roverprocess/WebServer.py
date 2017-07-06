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

# Rover Modules
from roverprocess.RoverProcess import RoverProcess
from threading import Thread
from multiprocessing import BoundedSemaphore

# WebUI Modules
import bottle
from bottle import run
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from WebUI.Routes import WebServerRoutes

# Python Modules
import time
import json
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

class WebServer(RoverProcess):

	def setup(self, args):
		for msg in ["RoverPosition", "RoverHeading"]:
			self.subscribe(msg)
		self.dataSem = BoundedSemaphore()
		self.data = {}
		self.routes = WebServerRoutes(parent=self, dataSem=self.dataSem)

		bottle.TEMPLATE_PATH = ['./WebUI/views']
		print("Web Templates Loaded From:", bottle.TEMPLATE_PATH)

		Thread(target = self.startBottleServer).start()

	def loop(self):
		#self.setShared("TestData", "hi!")
		time.sleep(1)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		#print(message)
		with self.dataSem:
			self.data.update(message)

	def cleanup(self):
		RoverProcess.cleanup(self)

	## Bottle server code running in independent thread
	# Please see routes.py for information about exchanging data
	def startBottleServer(self):
		run(host='localhost', port=8000, server=GeventWebSocketServer, app=self.routes.instance, debug=True)
