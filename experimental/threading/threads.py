# Fairly minimal example of how to do threading.

import threading
import time

# make a global flag we will use to ask threads to stop
threadExit = False

# We have to define a class for our threads.
# It needs functions called __init__ and run, but
# it can have any additional properties or functions we want it to.
# It extends the existing Thread class from threading.

class exampleThread(threading.Thread):
	# this is called when a thread object is created.
	def __init__(self, greeting, number):
		threading.Thread.__init__(self) # have to call inherited constructor first
		self.greeting = greeting
		self.number = number
	
	# this gets called when the thread is started
	def run(self):
		while not threadExit:
			print(str(self.greeting) + " from thread #" + str(self.number))
			time.sleep(1)
		print("thread #" + str(self.number) + " done")

# Word to the wise: never allow the same global / shared variable
# to be modified in multiple threads without proper synchronization.

# create the thread objects
threadOne = exampleThread("hello", 1)
threadTwo = exampleThread("YOLO", 2)

# start the threads
threadOne.start()
time.sleep(0.5)
threadTwo.start()

time.sleep(5)

# ask the other threads to stop
threadExit = True

print("main thread done")
# The main thread exits here. The process will terminate once all
# other threads have exited normally.

