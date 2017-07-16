from .RoverProcess import RoverProcess
import time


class Producer(RoverProcess):

    def loop(self):
        self.publish("ping", 1)
        time.sleep(0.0000001)

