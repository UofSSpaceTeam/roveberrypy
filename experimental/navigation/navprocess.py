from roverprocess import RoverProcess

import time
import Queue as Q

# navigation commands 
class navCommand(object):
    def __init__(self, priority, currentLoc, target):
        self.priority = priority
        self.stop = False
        #the current condition of rover (ie heading)
        self.current = current 
        # target condition of rover 
        self.target = target 
		
    def cancel(self):
        self.stop = True 
		
    def update(self, newCurrent):
        self.current = newCurrent

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)
	
class exampleCommand(navCommand):
    def run(self):
        #do something
        if self.current != self.target:
            print(self.current)
        else:
			self.cancel()			
			
class NavProcess(RoverProcess):
	
	def setup(self, args):
		self.start = True # should start false
		self.q = Q.PriorityQueue()
		#testing 
		self.q.put(exampleCommand(5, 0, 10))
		self.q.put(exampleCommand(1, 20, 30))
		self.command = None 
		self.count = 0
		
	def loop(self):
		if self.start is True: 
			self.runCommand()
		time.sleep(1)
	
	def messageTrigger(self, message):
		pass
	
	def cleanup(self):
		RoverProcess.cleanup(self)
	
	def runCommand(self):
	
		if self.command is not None:
			#testing
			self.command.run()
			self.count = self.command.current + 1
			self.command.update(self.count)
			if self.command.stop == True:
				self.command = None
		elif not self.q.empty():
			self.command = self.q.get()

	def addCommand(self, command):
		self.q.put(command)
	
	def removeAll(self):
		while not self.q.empty():
			self.q.get()

