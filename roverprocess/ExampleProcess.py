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

# Any libraries you need can be imported here. You almost always need time!
import time


class ExampleProcess(RoverProcess):
	# Some blank space to write functions, classes, threads - whatever you need.
	# There are no restrictions - this is your own process!

	# See the tutorials on the wiki for things like basic threads and custom libraries.
	# 	< TO DO: INSTERT LINK TO THAT WIKI AND WRITE IT >
	# This is a tool to communicate with the main state manager at startup.
	# 	It returns a dictionary of lists for all the incoming (self) and outgoing (server) messages
	#	so that the StateManager knows who gets what message.
	# Just put the name of the message in the relevant list.
	def getSubscribed(self):
		return ["heartbeat"]

	# This is run once to set up anything you need.
	# 	Hint: use the self object to store variables global to this process.
	# 	You can also take any args you need from the main startup as a dictionary:
	# 		self.something = args["something"]
	# 	This can be handy for sharing semaphores with other processes!
	def setup(self, args):
		self.someVariable = 42

	# This automatically loops forever.
	#	It is best to put a time.sleep(x) at the end. This makes sure that it
	#	will always run at the same time, and will give other processes time to run too!
	# Use self.setShared() to send some variables to another process or server!
	def loop(self):
		self.publish("test", 1)
		time.sleep(1)
		self.publish("test", 0)
		time.sleep(1)

	# This runs every time a new message comes in.
	#	It is often handy to have an if statement for every type of message you expect
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)

		if "heartbeat" in message:
			print("got: " + str(message["heartbeat"]))

	# This runs once at the end when the program shuts down.
	#	You can use this to do something like stop motors clean up open files
	def cleanup(self):
		# If you override this method, you must call RoverProcess.cleanup(self)
		RoverProcess.cleanup(self)

	# Whenever the "heartbeat" message is produced, the function "on_heartbeat"
	# is called. This is an alternative to using large if/else structures in
	# messageTrigger. In this function, message is the contents of the message,
	# not the dictionary that contains multiple keys like in messageTrigger.
	def on_heartbeat(self, message):
		print("From callback got: " + str(messsage))


