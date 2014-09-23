import subprocess
import socket
import time

	# constants

commandPort = 3000
videoPort = 3001

	# functions

def startCamera():
	command = "raspivid -b 500000 -n -ex fixedfps -fps 8 -t 0 -rot 180 -o - | nc " + clientAddress[0] + " " + str(videoPort)
	#print(command)
	subprocess.Popen(command, shell = True, stderr = open("/dev/null", "w"))

def stopCamera():
	command = "sudo killall nc; sudo killall raspivid"
	#print(command)
	try:
		subprocess.call(command, shell = True, stdout = open("/dev/null", "w"), stderr = open("/dev/null", "w"))
	except:
		pass

def parseCommand(command):
	if(len(command) > 2 and command[0] == "#"): # is valid
		if(command[1] == "C"):
			if(command[2] == "S"): #CS
				print("starting camera feed")
				startCamera()
			elif(command[2] == "E"): #CE
				print("stopping camera feed")
				stopCamera()
			elif(command[2]== "P"): #CP
				print("taking picture")
				takePicture()

def takePicture():
	command = "raspistill -t 1000 -rot 180 -o /home/pi/pictures/" + time.strftime("%m%d%H%M%S", time.localtime()) + ".jpg"
	subprocess.call(command, shell = True)

def stopSockets():
	try:
		commandSocket.close()
	except:
		pass
	try:
		serverSocket.close()
	except:
		pass

def quit():
	stopCamera()
	stopSockets()
	exit(0)

### Main Program  ###

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	serverSocket.bind(("", commandPort))
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serverSocket.listen(0)
	print("Camera Server listening on port " + str(commandPort))
	while(True):
		(commandSocket, clientAddress) = serverSocket.accept()
		print("Camera Server connected.")
		while(True):
			try:
				data = commandSocket.recv(256)
			except socket.error:
				stopCamera()
				break
			if(data == ""): # socket closing
				stopCamera()
				break
			else:
				parseCommand(data)
		print("Camera Server disconnected.")
	
except KeyboardInterrupt:
	print("\nmanual shutdown...")
	quit()
except: 
	raise
	quit()

