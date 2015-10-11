from roverprocess import RoverProcess
from threading import Thread

import time
from libs.bottle import route, run, template, ServerAdapter

class WebserverProcess(RoverProcess):
	
	## Replaces the stock WSGI server with one that we can control within
	##	the context of the rover software
	class RoverWSGIServer(ServerAdapter):
		
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
		self.server = self.RoverWSGIServer(host='localhost', port=8080)
		Thread(target = self.startBottleServer).start()

	def loop(self):
		time.sleep(1)
	
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		#if "exampleKey" in message:
		#	print "got: " + str(message["exampleKey"])
	
	def cleanup(self):
		RoverProcess.cleanup(self)
		
	## Bottle server code running in independent thread
	##	TODO: Send and recieve data from the main software!
		
	def startBottleServer(self):
		@route('/hello/<name>')
		def index(name):
			return template('<b>Hello {{name}}</b>!', name=name)
		
		run(server=self.server)
		