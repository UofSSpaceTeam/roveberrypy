from RoverProcess import RoverProcess

import time
import smbus

class CommandType:
    MANUAL = 0x00
    INVERSE_KIN = 0x01
    GET_FEEDBACK = 0x02

class Command:
    def __init__(self):
        self.type = 0x00
        self.position = [0,0,0]
        self.duty_cycle = [0,0,0,0,0,0]

    def csum(self):
        return (sum(self.position) + sum(self.duty_cycle)) % 256

class ArmProcess(RoverProcess):

    def getSubscribed(self):
        return {
                "self" : ["axes"],
                "json" : [],
                "can" : [],
                "web" : []
                }

    def setup(self, args):
        self.i2c = smbus.SMBus(1)
        self.address = 0x07
        self.i2cSem = args["sem"]
        self.update = False
        self.feedback = [0,0]
        self.dutys = [0,0,0,0,0,0]
        self.positions = [0,0,0]

    def loop(self):
        val = False
        while(True):
            self.update = True
            c = Command();
            c.type = CommandType.INVERSE_KIN
            c.position = [300,2,-512]
            c.duty_cycle = self.dutys
            c.position = self.positions
            self.sendCommand(c)
            #temp_feedback = self.requestPosition()
            #if not None in temp_feedback:
            #    self.feedback = temp_feedback
            #else:
            #    print("got invalid data");
            time.sleep(0.1)

    def messageTrigger(self, message):
        RoverProcess.messageTrigger(self, message)
        if "axes" in message:
            self.dutys = [int(float(x)*127) for x in message["axes"]]

    def sendCommand(self, command):
        #break command.position into 6 8-bit values, lsb first
        buff = [0, 0, 0, 0, 0, 0]
        for i in range(0,5,2):
            buff[i] = command.position[i/2] & 0x00FF
            buff[i+1] = (command.position[i/2] & 0xFF00) >> 8

        #print(command.duty_cycle)
        try:
            self.i2cSem.acquire(block=True, timeout=None)
            print(command.csum())
            self.i2c.write_i2c_block_data(self.address, command.type,
                    buff + command.duty_cycle + [command.csum()])
        except:
            print("Arm thread got an I2C error")
        self.i2cSem.release()


    def requestPosition(self):
        position = [None,None]
        try:
            self.i2cSem.acquire(block=True, timeout=None)
            buffer = []
            buffer = self.i2c.read_i2c_block_data(self.address, CommandType.GET_FEEDBACK, 4)
            for i in range(1,5,2):
                position[(i-1)/2] = buffer[i-1] & 0x00FF
                position[(i-1)/2] |= (buffer[i] << 8) & 0xFF00
            print(position)
            print("\n")

        except:
            print("Arm thread got an I2C error")
        self.i2cSem.release()
        return position


    def cleanup(self):
        RoverProcess.cleanup(self)

