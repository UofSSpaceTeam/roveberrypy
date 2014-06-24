from ServoDriver import *
import socket
import time

drivePort = 3002
stopValue = 1710

def setSpeed(leftSpeed, rightSpeed):#4-6 left side 9-11 right side
	leftSpeed = int((leftSpeed*4.6)) + stopValue
	rightSpeed = int((rightSpeed*4.6)) + stopValue
	if leftSpeed > 2200:
		leftSpeed = 2200
	if leftSpeed < 1200:
		leftSpeed = 1200
	if rightSpeed > 2200:
		rightSpeed = 2200
	if rightSpeed < 1200:
		rightSpeed = 1200
	#print leftSpeed
	#print rightSpeed
	servoDriver.setServo(4,leftSpeed)
	servoDriver.setServo(5,leftSpeed)
	servoDriver.setServo(6,leftSpeed)
	servoDriver.setServo(9, rightSpeed)
	servoDriver.setServo(10, rightSpeed)
	servoDriver.setServo(11, rightSpeed)

def parseCommand(command): # parses and executes remote commands
	if command != None:
		if len(command) > 2:
			if command[0] == "#": # is valid
				if command[1] == "D":
					if command[2] == "1" and len(command) > 5: # one stick drive
						xChar = int(ord(command[3]))
						yChar = int(ord(command[4]))
						limit = int(ord(command[5]))
						leftSpeed = -(yChar + xChar - 254)
						rightSpeed = yChar - xChar
						if max(abs(leftSpeed), abs(rightSpeed)) > limit:
							scaleFactor = float(limit) / max(abs(leftSpeed), abs(rightSpeed))
						else:
							scaleFactor = 1
						leftSpeed *= scaleFactor
						rightSpeed *= scaleFactor
						setSpeed(leftSpeed, rightSpeed)
					elif command[2] == "2" and len(command) > 4: # two stick drive
						leftSpeed = -(int(ord(command[3])) - 127)
						rightSpeed = int(ord(command[4])) - 127
						setSpeed(leftSpeed, rightSpeed)
					elif command[2] == "S": # Stop
						stopServos()
						#print("motors stopped.")
					elif command[2] == "D": # Dig
						print("digging...")
						stopServos()
						servoDriver.setServo(4, 2200)
						time.sleep(0.8)
						servoDriver.setServo(4, stopValue)
						time.sleep(0.2)
						servoDriver.setServo(4, 1200)
						time.sleep(0.8)
						stopServos()
						print "done"
	else: # command == none
		stopServos()
		
def stopServos():
	servoDriver.setServo(4, stopValue)
	servoDriver.setServo(5, stopValue)
	servoDriver.setServo(6, stopValue)
	servoDriver.setServo(9, stopValue)
	servoDriver.setServo(10,stopValue)
	servoDriver.setServo(11,stopValue)
	
def stopSockets():
	try:
		driveSocket.close()
	except:
		pass
	try:
		serverSocket.close()
	except:
		pass
		
def quit():
	stopServos()
	stopSockets()
	
#Start Servos
servoDriver = ServoDriver()
	
# begin server connection
try:
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serverSocket.bind(("", drivePort))
	serverSocket.listen(0)
	print("Drive Server listening on port " + str(drivePort))
	while(True):
		(driveSocket, clientAddress) = serverSocket.accept()
		print("Drive Server connected.")
		driveSocket.settimeout(1.0)
		while(True):
			try:
				data = driveSocket.recv(256)
				if(data == ""): # socket closing
					stopServos()
					break
				else:
					parseCommand(data)
			except socket.timeout:
				stopServos()
		print("Drive Server disconnected.")
	
except KeyboardInterrupt:
	print("\nmanual shutdown...")
	quit()
	exit(0)
except:
	quit()
	raise
