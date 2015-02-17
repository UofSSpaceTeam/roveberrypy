
import roverMessages
import threading
import json
from Queue import Queue
import time
import unicodeConvert
import smbus

convert = unicodeConvert.convert
i2c = smbus.SMBus(1)
address = 0x07

class driveThread(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
                self.name = "driveThread"
                self.exit = False
                self.mailbox = Queue()

        def run(self):
                while not self.exit:
                        if not self.mailbox.empty():
                                data = self.mailbox.get()
                                if "c1t" in data:
                                        val = int(data.pop()*100 + 100)
                                        i2c.write_byte(address, hex(val))
                        else:
                                pass
                                #print "No Data!"
                        time.sleep(0.01)

        def stop(self):
                self.exit = True