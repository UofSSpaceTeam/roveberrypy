from roverprocess import RoverProcess

import time
from libs.bottle import route, run, template

class WebserverProcess(RoverProcess):
	
	# helper classes go here if you want any
	
	def setup(self, args):
		@route('/hello/<name>')
		def index(name):
			return template('<b>Hello {{name}}</b>!', name=name)
	
		run(host='localhost', port=8080)

	def loop(self):
		time.sleep(1)
	
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		# your message handling here. for example:
		if "exampleKey" in message:
			print "got: " + str(message["exampleKey"])
	
	def cleanup(self):
		RoverProcess.cleanup(self)
		# your cleanup code here. e.g. stopAllMotors()
	
	# additional functions go here
		