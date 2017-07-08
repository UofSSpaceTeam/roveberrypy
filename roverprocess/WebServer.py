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
#from WebUI.bottle.ext.websocket import GeventWebSocketServer
#from WebUI.bottle.ext.websocket import websocket
from WebUI.Routes import WebServerRoutes
from bottle import ServerAdapter

# Python Modules
import time
import json
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

class WebServer(RoverProcess):
	## Replaces the stock WSGI server with one that we can control within
	##	the context of the rover software
	class RoverWSGIServer(ServerAdapter):
		quiet = False # comment this out for verbose logging

		def run(self, app):  # pragma: no cover
			from wsgiref.simple_server import make_server
			from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
			import socket

			class FixedHandler(WSGIRequestHandler):
				def address_string(self):  # Prevent reverse DNS lookups please.
					return self.client_address[0]

				def log_request(*args, **kw):
					if not self.quiet:
						return WSGIRequestHandler.log_request(*args, **kw)

			handler_cls = self.options.get('handler_class', FixedHandler)
			server_cls = self.options.get('server_class', WSGIServer)

			if ':' in self.host:  # Fix wsgiref for IPv6 addresses.
				if getattr(server_cls, 'address_family') == socket.AF_INET:

					class server_cls(server_cls):
						address_family = socket.AF_INET6

			self.srv = make_server(self.host, self.port, app, server_cls,
								   handler_cls)
			self.port = self.srv.server_port
			self.srv.serve_forever()


	def setup(self, args):
		for msg in ["RoverPosition", "RoverHeading"]:
			self.subscribe(msg)
		self.dataSem = BoundedSemaphore()
		self.data = {}
		self.routes = WebServerRoutes(parent=self, dataSem=self.dataSem)

		bottle.TEMPLATE_PATH = ['./WebUI/views']
		print("Web Templates Loaded From:", bottle.TEMPLATE_PATH)
		self.server = self.RoverWSGIServer(host='3.3.3.4', port=8000)


		Thread(target = self.startBottleServer).start()

	def loop(self):
		#self.setShared("TestData", "hi!")
		time.sleep(1)

	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		with self.dataSem:
			self.data[message.key] = message.data

	def cleanup(self):
		RoverProcess.cleanup(self)

	## Bottle server code running in independent thread
	# Please see routes.py for information about exchanging data
	def startBottleServer(self):
		run(server=self.server, app=self.routes.instance)
