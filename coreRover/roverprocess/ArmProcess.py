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
                "self" : ["axes", "arm_mode"],
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
        self.command = Command()
        self.command.type = CommandType.MANUAL
        self.command.position = [0,0,0]
        self.command.duty_cycle = [0,0,0,0,0,0]

    def loop(self):
        while(True):
            self.update = True
            #self.sendCommand(self.command)
            #self.requestPosition()
            #print(self.feedback)
            time.sleep(0.1)

    def messageTrigger(self, message):
        RoverProcess.messageTrigger(self, message)
        if "arm_mode" in message:
            if message["arm_mode"] == CommandType.GET_FEEDBACK:
                self.requestPosition()
            else:
                self.command.type = message["arm_mode"]

        if "axes" in message:
            if self.command.type == CommandType.MANUAL:
	        self.command.duty_cycle = \
                     [int(float(x)*127) for x in message["axes"]] + [0,0]
            elif self.command.type  == CommandType.INVERSE_KIN:
                #change these to suit control scheme
                self.command.position[0] = int(float(message["axes"][0])*127)
                self.command.position[1] = int(float(message["axes"][1])*127)
                self.command.position[2] = int(float(message["axes"][2])*127)
            self.sendCommand(self.command)

    def sendCommand(self, command):
        #break command.position into 6 8-bit values, lsb first
        buff = [0, 0, 0, 0, 0, 0]
        for i in range(0,5,2):
            buff[i] = command.position[i/2] & 0x00FF
            buff[i+1] = (command.position[i/2] & 0xFF00) >> 8

        print(buff + [11111111] +  command.duty_cycle)
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
            if None in position:
                print("Arm got invalid feedback")
            else:
                self.feedback = position
            #print(position)
            #print("\n")

        except:
            print("Arm thread got an I2C error")
        self.i2cSem.release()


    def cleanup(self):
        RoverProcess.cleanup(self)
