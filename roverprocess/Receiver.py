from .RoverProcess import RoverProcess
from multiprocessing import Semaphore
import time


class Receiver(RoverProcess):
    def setup(self, args):
        self.counter = 0
        self.sem = Semaphore()
        self.subscribe("ring")

    def loop(self):
        time.sleep(1)
        self.sem.acquire()
        self.log(self.counter)
        self.counter = 0
        self.sem.release()

    def on_ring(self, data):
        self.sem.acquire()
        self.counter += 1
        self.sem.release()


