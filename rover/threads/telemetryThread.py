import threading
from Queue import Queue
import time
import serial 

class TelemetryThread(threading.Thread):
        def __init__(self, parent):
                threading.Thread.__init__(self)
                self.parent = parent
                self.name = "telemetryThread"
                self.exit = False
                self.commThread = None
                self.mailbox = Queue()
                
        def run(self):
                while True:
						msg = {} 
						#print(msg)
						# get info from sensor every 1 sec
						time.sleep(1)
						msg.update(self.sensorInfo())
						
						if msg["gx"] is None:
								print("error in packet")
						else:
								print("packet good")
								#print(msg)
								self.parent.commThread.mailbox.put(msg)
                        
        # simulates receiving info from a sensor                
        def sensorInfo(self):
                # set up serial, Serial(port, buadrate)
                # will need to be change when on rover 
                ser = serial.Serial("/dev/ttyAMA0",9600, timeout=1)
                #ser = serial.Serial("COM9", 9600, timeout=1 )
                value = {}
                # read data from serial (USB)
				try:
					str = ser.readline()
                except:
					value["gx"] = None
					return value
				
				
                # prints in the order pitch roll gx gy gz ax ay az heading aroll apitch lat lon mps alt gps_heading date time vout isense
                data = str.split();
                
				#make sure packet is complete 
                if len(data) != 21:
					value["gx"] = None
					return value 

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
                value["isense"] = data[19]
				
                speed = float(value["mps"]) * 60
				
                value["roverGPS"] = [value["lat"], value["lon"], speed, value["gps_heading"]]
                vaulue["towerGPS"] = [value["lat"], value["lon"]]
				
                checksum = data[20].rstrip("$")

                #if float(checksum) == self.checksum( float(value["roll"]), float(value["time"]), float(value["heading"])):
                return value
                #else:
                        #print("Error: invalid packet")
                        #value in gx arbitrary picked to send error 
                        #value["gx"] = None
                        #return value
                        
                
                
        def checksum(self, a, b, c):
                sum = a * b * c
                return sum % 256 
                

        def stop(self):
				self._Thread__stop()
