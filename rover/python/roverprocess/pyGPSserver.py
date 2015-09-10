import socket
from libs.sbp.pyserial_driver import PySerialDriver

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('192.168.1.103', 10000)
print 'starting up on %s port %s' % server_address
sock.bind(server_address)

import argparse
parser = argparse.ArgumentParser(description="Swift Navigation SBP Example.")
parser.add_argument("-p", "--port",
	default=['/dev/ttyUSB0'], nargs=1,
	help="specify the serial port to use.")
args = parser.parse_args()

driver = PySerialDriver(args.port[0], baud=1000000)

class NMEAPoint:
	 def __init__(self):
		self.lat = 0
		self.lng = 0
		self.hdg = 0
		self.hdop = 0

def readGPS_NMEA():
		p = NMEAPoint()
		rawData = driver.handle.read(driver.handle.inWaiting())
		dataStart = rawData.find("GGA")
		if dataStart != -1:	# found start of valid sentence
			dataEnd = min(dataStart + 70, len(rawData) - dataStart - 2)
			data = rawData[dataStart:dataEnd]
			values = data.split(",")
			if len(values) > 9:
				p.lat = float(values[2][:2])
				p.lat += float(values[2][2:])/60
				p.lng = float(values[4][:3])
				p.lng += float(values[4][3:])/60
				p.hdop = float(values[8])
				#altitude = float(values[9])
		return p

while True:
	print 'waiting to receive message'
	data, address = sock.recvfrom(4096)
	
	print 'received %s bytes from %s' % (len(data), address)
	print  data
	
	try:
		p = readGPS_NMEA()
		data = str(p.lat) + ' ' + str(p.lng)
	
	except:
		print "Serial Error"
	
	if data:
		sent = sock.sendto(data, address)
		print 'sent %s bytes back to %s' % (sent, address)
