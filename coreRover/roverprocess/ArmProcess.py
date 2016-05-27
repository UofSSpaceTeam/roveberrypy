from RoverProcess import RoverProcess

import time
import smbus

class CommandType:
    MANUAL = 0x00
    INVERSE_KIN = 0x01

class Command:
    def __init__(self):
        self.type = 0x00
        self.position = [0,0,0]
        self.velocity = [0,0,0,0,0,0]

    def csum(self):
        return (sum(self.position) + sum(self.velocity)) % 256

class ArmProcess(RoverProcess):

    def getSubscribed(self):
        return {
                "self" : [],
                "json" : [],
                "can" : [],
                "web" : []
                }

    def setup(self, args):
        self.i2c = smbus.SMBus(1)
        self.address = 0x07
        self.i2cSem = args["sem"]
        self.update = False

    def loop(self):
        val = False
        while(True):
            self.update = True
            c = Command();
            c.type = CommandType.INVERSE_KIN
            c.position = [3,1,1]
            c.velocity = [60,50,40,30,20,10]
            self.sendCommand(c)
            time.sleep(3)

    def messageTrigger(self, message):
        RoverProcess.messageTrigger(self, message)

    def sendCommand(self, command):

            try:
                self.i2cSem.acquire(block=True, timeout=None)
                print(command.csum())
                self.i2c.write_i2c_block_data(self.address, command.type,
                        command.position + command.velocity + [command.csum()])
            except:
                print("Arm thread got an I2C error")
            self.i2cSem.release()

    def cleanup(self):
        RoverProcess.cleanup(self)

