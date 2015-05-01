import roverMessages as messages
import threading
import json
from Queue import Queue
import time
from unicodeConvert import convert
import serial 

class telemetryThread(threading.Thread):
        def __init__(self, parent):
                threading.Thread.__init__(self)
                self.parent = parent
                self.name = "telemetryThread"
                self.exit = False
                self.commThread = None
                self.mailbox = Queue()
                # set up serial, Serial(port, buadrate)
                # will need to be change when on rover 
                #ser = serial.Serial("COM7", 115200)

                
        def run(self):
                while not self.exit:
                        msg = {} 
                        #print(msg)
                        # get info from sensor every 1 sec
                        time.sleep(1)
                        msg.update(self.sensorInfo())
                        
                        if value["gx"] is None:
                                print("error in packet")
                        else:
                                print("packet good")
                                self.parent.commThread.mailbox.put(msg)
                        
        # simulates receiving info from a sensor                
        def sensorInfo(self):
                # set up serial, Serial(port, buadrate)
                # will need to be change when on rover 
                ser = serial.Serial("COM7", 115200)
                value = {}
                #add values to test
                #using c1j1y arbitrarily 
                #value["c1j1y"] = 0.5
                # read data from serial (USB)
                str = ser.readline() 
                # TODO: parse data and send it through mailbox 
                # TODO: add checksum 
                # prints in the order pitch roll gx gy gz ax ay az heading aroll apitch lat lon mps alt gps_heading date time vout isense
                data = str.split();
                #print(data)
                
                value["pitch"] = data[0].lstrip("#")
                value["roll"] = data[1]
                value["gx"] = data[2]
                value["gy"] = data[3]
                value["gz"] = data[4]
                value["ax"] = data[5]
                value["ay"] = data[6]
                value["az"] = data[7]
                value["heading"] = data[8]
                value["aroll"] = data[9]
                value["apitch"] = data[10]
                value["lat"] = data[11]
                value["lon"] = data[12]
                value["mps"] = data[13]
                value["alt"] = data[14]
                value["gps_heading"] = data[15]
                value["date"] = data[16]
                value["time"] = data[17]
                value["vout"] = data[18]
                value["isense"] = data[19].rstrip("$")

                print(data[19])
                print(self.checksum( float(value["roll"]), float(value["time"]), float(value["heading"])))

                if float(data[19]) == self.checksum( float(value["roll"]), float(value["time"]), float(value["heading"])):
                        return value
                else:
                        print("Error: invalid packet")
                        #value in gx arbitrary picked to send error 
                        value["gx"] = None
                        return value
                        
                
                
        def checksum(self, a, b, c):
                sum = a * b * c
                return sum % 256 
                

        def stop(self):
                self.exit = True
