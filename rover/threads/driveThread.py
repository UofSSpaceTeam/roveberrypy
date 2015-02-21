
import roverMessages
import threading
import json
from Queue import Queue
import time
import unicodeConvert
import smbus

convert = unicodeConvert.convert

# Setting up I2C
i2c = smbus.SMBus(1)
address = 0x07

# I2C Commands List
# Mtoror sub-addresses for manual mode
RF = 0xF1
RC = 0xF2
RR = 0xF3
LF = 0xF4
LC = 0xF5
LR = 0xF6

# Commands
STOP = 0xF7 
OS = 0xF8 #one-stick
TS = 0xF9 #two-stick
MAN = 0xF0 #manual mode toggle
A = 0xFA #stick A
B = 0xFB #stick B

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
                                    i2c.write_byte(address, A)
									val = int(data.pop()*100 + 100) #gives us a range of 0-100
									i2c.write_byte(address, val)
								else if "c1j2y" in data:
									i2c.write_bute(address, B)
									val = int(data.pop()*100 + 100)
									i2c.write_byte(address, val)
                        else:
                                pass
                                #print "No Data!"
                        time.sleep(0.01)

        def stop(self):
                self.exit = True