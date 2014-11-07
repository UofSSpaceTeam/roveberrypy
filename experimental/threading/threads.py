import threading
import time

# global flag used to ask threads to stop
threadExit = False

# First we have to define a class for our threads.
# It needs functions called __init__ and run, but
# it can have any additional properties or functions we want it to.
# It extends the existing Thread class from threading.

class genericThread(threading.Thread):
	# this is called when a thread object is created.
	def __init__(self, function, args):
		threading.Thread.__init__(self) # first, call the inherited constructor
		self.function = function # the function the thread will run
		self.args = args # tuple of arguments to call the function with
	
	# this gets called when the thread is started
	def run(self):
		self.function(self.args)

# end of our thread class.

# make a function for our new threads to start at
# note the double parens since args (above) will be a tuple.
def someFunction((greeting, number)):
	while True:
		if threadExit:
			print("thread " + str(number) + " done")
			return
		print(str(greeting) + " from thread " + str(number))
		time.sleep(1)

# create the thread objects
threadOne = genericThread(someFunction, ("hello", 1))
threadTwo = genericThread(someFunction, ("YOLO", 2))

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

