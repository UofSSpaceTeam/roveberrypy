# example of sending messages between threads via queues.

import threading
from Queue import Queue
import time
from random import Random

threadExit = False

# make a thread type that produces and transmits random data
class workerThread(threading.Thread):
	def __init__(self, seed, dest):
		threading.Thread.__init__(self)
		self.dest = dest # destination mailbox
		self.seed = seed
		self.rng = Random(seed)
	
	def run(self):
		while not threadExit:
			data = self.rng.randint(self.seed, 2 * self.seed)
			self.dest.put(data)
			time.sleep(0.5)

# make a thread type that periodically receives and prints data
class printerThread(threading.Thread):
	def __init__(self, capacity):
		threading.Thread.__init__(self)
		self.mailbox = Queue(capacity) # queue used to receive messages
		
	def run(self):
		while not threadExit:
			while not self.mailbox.empty():
				print(str(self.mailbox.get()))
			time.sleep(1)

# create the thread objects
printer = printerThread(100)
workerOne = workerThread(50, printer.mailbox)
workerTwo = workerThread(100, printer.mailbox)

# start the threads
printer.start()
workerOne.start()
workerTwo.start()

time.sleep(5)
threadExit = True
print("exiting")

