from .RoverProcess import RoverProcess
from multiprocessing import Semaphore
import time


class Consumer(RoverProcess):
    def setup(self, args):
        self.counter1 = 0
        self.sem1 = Semaphore()
        self.counter2 = 0
        self.sem2 = Semaphore()
        self.subscribe("ping")
        self.subscribe("ring")

    def loop(self):
        time.sleep(1)
        self.sem1.acquire()
        self.log("ping: {}".format(self.counter1))
        self.counter1 = 0
        self.sem1.release()
        self.sem2.acquire()
        self.log("ring: {}".format(self.counter2))
        self.counter2 = 0
        self.sem2.release()

    def on_ping(self, data):
        self.sem1.acquire()
        self.counter1 += 1
        self.sem1.release()

    def on_ring(self, data):
        self.sem2.acquire()
        self.counter2 += 1
        self.sem2.release()
