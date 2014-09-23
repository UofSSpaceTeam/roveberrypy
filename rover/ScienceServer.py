import math
import socket
import time
import subprocess
from ServoDriver import *
import RPi.GPIO as GPIO # for hardware reset system

sciencePort = 3006

# do SCIENCE!
def runExperiment():
	experpos = 1700 # position to drop soil into experiment chamber
	samppos = 2100 # position to drop soil into sample chamber
	shakenum = 10 # number of times to "shake" servo before moving on
	shakeammount = 50
	command = "raspistill -o /home/pi/pictures/exp_%d.jpg -tl 2000 -t 60000"
	print("we are sciencing")
	#setup servo
	servoDriver = ServoDriver()
	#move to position to drop soil into experiment chamber
	servoDriver.setServo(4,experpos)
	GPIO.output(16,True)
	time.sleep(0.5)
	
	
	# "shake" servo to get more soil in 
	for i in range(0,shakenum):
		servoDriver.setServo(4, experpos + shakeammount)
		time.sleep(0.05)
		servoDriver.setServo(4, experpos - 2*shakeammount)
		time.sleep(0.05)
		servoDriver.setServo(4, experpos + 2*shakeammount)
		time.sleep(0.1)
	#take picture
	servoDriver.setServo(4,samppos)
	subprocess.call(command, shell = True)
	GPIO.output(16,False)
	print("Sciencing has been completed")
	# #move to position to drop soil into sample chamber
	# servoDriver.setServo(4,samppos)
	
	# # "shake" servo to get more soil in 
	# for i in range(0,shakenum)
		# servoDriver.setservo(4, samppos + shakeammount)
		# time.sleep(0.1)
		# servoDriver.setservo(4, samppos - 2*shakeammount)
		# time.sleep(0.1)
		# servoDriver.setservo(4, samppos + 2*shakeammount)
		# time.sleep(0.1)

	
def parseCommand(command):
#	print(command)
	if command == "#RE":
		runExperiment()

def stopSockets(): # Stops sockets on error condition
	try:
		scienceSocket.close()
	except:
		pass
	try:
		serverSocket.close()
	except:
		pass


### Main Program ###

# set up logging
try:
	logfile = open("/home/pi/scienceLogs/" + time.strftime("%m%d%H%M%S", time.localtime()) + ".log", "w")
except:
	print("science logging failed!")

# set up GPIOs
# try:
	# GPIO.setwarnings(False)
	# GPIO.setmode(GPIO.BOARD)
	# GPIO.setup(11, GPIO.OUT) # stepper direction
	# GPIO.setup(13, GPIO.OUT) # stepper step
# except:
	# print("GPIO setup failed!")
	# raise
	# #subprocess.call("sudo reboot", shell = True)
	
# begin server connection
try:
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serverSocket.bind(("", sciencePort))
	serverSocket.listen(0)
	
	#set up gpio
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(16,GPIO.OUT)
	GPIO.output(16,False)	# have light set to off
	print("Science Server listening on port " + str(sciencePort))
	# main execution loop
	while(True):
		(scienceSocket, clientAddress) = serverSocket.accept()
		print("Science Server connected.")
		while(True):
			data = scienceSocket.recv(256)
			if(data == ""): # socket closing
				break
			else:
				parseCommand(data)
		print("Science Server disconnected.")
except KeyboardInterrupt:
	print("\nmanual shutdown...")
	stopSockets()
	#GPIO.cleanup()
except:
	stopSockets()
	#GPIO.cleanup()
	raise
