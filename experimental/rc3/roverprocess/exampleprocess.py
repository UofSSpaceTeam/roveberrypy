import RoverProcess

# your imports go here. For example:
import time
from threading import Thread

# Built-in RoverProcess API:
# get(key): look for the attribute called "key"

class ExampleProcess(RoverProcess):
	
	# any helper classes go here. for example:
	class exampleThread(Thread):
		pass
	
	def __init__(self, **kwargs):
		RoverProcess.__init__(self, kwargs)
		# your argument processing here. for example:
		self.something = kwargs["something"]
		# move other initialization to setup() to avoid problems.
	
	def setup(self):
		# your setup code here. for example:
		example = exampleThread()
	
	def loop(self):
		# your looping code here. for example:
		time.sleep(1)
	
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		# your message handling here. for example:
		if "exampleThing" in message:
			self.exampleFunction(message["exampleThing"])
	
	def cleanup(self):
		RoverProcess.cleanup(self)
		# your cleanup code here. e.g. stop all the motors!
	
	# your functions go here

	