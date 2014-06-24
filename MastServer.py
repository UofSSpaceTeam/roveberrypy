from ServoDriver import *
import socket
import time

mastPort = 3004
currentPitch = 1300

def parseCommand(command): # parses and executes remote commands
	if command != None:
		if len(command) > 2:
			if command[0] == "#": # is valid
				if command[1] == "M":
					if command[2] == "C": # Camera look
						x_dPad = int(ord(command[3])) - 2	#vertical d-Pad button
						y_dPad = int(ord(command[4])) - 2	#horizontal d-Pad button
						moveServos(x_dPad, y_dPad)
					elif command[2] == "S": # Stop
						stopServos()
	else: # command == none
		stopServos()

def moveServos(yaw, pitch):
	global currentPitch
	#print str(yaw)
	#print str(pitch)
	currentPitch += 50 * pitch
	if currentPitch > 2300:
		currentPitch = 2300
	if currentPitch < 780:
		currentPitch = 780
	servoDriver.setServo(3, int(currentPitch))
	if yaw > 0:
		servoDriver.setServo(1, 1565)
	if yaw < 0:
		servoDriver.setServo(1, 1535)
	time.sleep(0.1)
	stopServos()

def stopServos():
	try:
		servoDriver.setServo(1, 1550)
	except:
		pass
		
def stopSockets():
	try:
		mastSocket.close()
	except:
		pass
	try:
		serverSocket.close()
	except:
		pass

def quit():
	stopServos()
	stopSockets()
		
### Main Program  ###

# set up servo driver
servoDriver = ServoDriver()
servoDriver.setServo(1, 1550)
servoDriver.setServo(3, int(currentPitch))
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
try:
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serverSocket.bind(("", mastPort))
	serverSocket.listen(0)
	print("Mast Server listening on port " + str(mastPort))
	while(True):
		(mastSocket, clientAddress) = serverSocket.accept()
		print("Mast Server connected.")
		mastSocket.settimeout(0.5)
		while(True):
			try:
				data = mastSocket.recv(256)
				if(data == ""): # socket closing
					stopServos()
					break
				else:
					parseCommand(data)
			except socket.timeout:
				time.sleep(0.25)
		print("Mast Server disconnected.")
	
except KeyboardInterrupt:
	print("\nmanual shutdown...")
	quit()
except:
	quit()
	raise
