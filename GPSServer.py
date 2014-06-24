import serial
import socket
import time
import struct

GPSPort = 3005
header = "#GD" #GPS Data
lastSendTime = 0.0
gps = None
logfile = None

latitude = None
longitude = None
latmin = None
lonmin = None
altitude = None
hdop = None

def readGPS():
	global gps, latitude, latmin, longitude, lonmin, altitude, hdop
	rawData = gps.read(gps.inWaiting())
	dataStart = rawData.find("GGA")
	if dataStart != -1:	# found start of valid sentence
		dataEnd = min(dataStart + 70, len(rawData) - dataStart - 2)
		data = rawData[dataStart:dataEnd]
		values = data.split(",")
		if len(values) > 9:
			latitude = float(values[2][:2])
			latmin = float(values[2][2:])
			longitude = float(values[4][:3])
			lonmin = float(values[4][3:])
			hdop = float(values[8])
			altitude = float(values[9])

def sendData():
	global latitude, longitude, latmin, lonmin, altitude, hdop, dataSocket, logfile#, course
	if latitude != None and longitude != None and altitude != None and hdop != None:
		dataSocket.send(struct.pack("!ffffff", latitude, latmin, longitude, lonmin, altitude, hdop))
		try:
			logfile.write(str(latitude) + " " + str(latmin) + "," + str(longitude) + " " + str(lonmin) + "," + str(altitude) + "," + str(hdop) + "\n")
		except:
			pass
	
def stopSockets():
	try:
		dataSocket.close()
	except:
		pass
	try:
		serverSocket.close()
	except:
		pass

def stopGPS():
	try:
		gps.close()
	except:
		pass

def stopLog():
	try:
		logfile.close()
	except:
		pass

def quit():
	stopGPS()
	stopLog()
	stopSockets()

### Main Program ###

# set up logging
try:
	logfile = open("/home/pi/gpsLogs/" + time.strftime("%m%d%H%M%S", time.localtime()) + ".log", "w+")
except:
	print("GPS logging failed.")
	pass

# set up serial connection
try:
	gps = serial.Serial("/dev/ttyAMA0", bytesize = 8, parity = 'N', stopbits = 1)
	gps.baudrate = 9600
	gps.timeout = 0.2
except:
	print("GPS setup failed!")
	quit()

# start socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
	serverSocket.bind(("", GPSPort))
	serverSocket.listen(0)
	print("GPS Server listening on port " + str(GPSPort))
	while(True):
		(dataSocket, clientAddress) = serverSocket.accept()
		print("GPS Server connected.")
		while(True):
			time.sleep(2.0)
			try:
				readGPS()
				sendData()
			except:
				break	
		print("GPS Server disconnected.")
	
except KeyboardInterrupt:
	print("\nmanual shutdown...")
	quit()
	exit(0)
except:
	quit()
	raise

