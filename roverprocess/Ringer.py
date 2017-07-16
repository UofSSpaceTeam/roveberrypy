from .RoverProcess import RoverProcess
import time


class Ringer(RoverProcess):

    def loop(self):
        self.publish("ring", 1)
        time.sleep(0.0000001)

