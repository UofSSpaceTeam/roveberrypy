# A script continuously run by the arm control pi.

import socket
import time
import serial
from ServoDriver import *
from ADS1x15 import ADS1x15
from Adafruit_I2C import Adafruit_I2C
import RPi.GPIO as GPIO # for hardware reset system

# global constants	

armPort = 3003
ramping = 10
scaleFactor = 0.55
address = 128
L1LowerLimit = 320
L2LowerLimit = 318

#actuator parameters
ActuatorFullIn = 292.354	#lengths again in mm
ActuatorFullOut = 444.754

Actuator1FullInRaw = 243
Actuator1FullOutRaw = 4749

Actuator2FullInRaw = 1890
Actuator2FullOutRaw = 3081

# function definitions

def readActuator1():
	#reads adc and maps the result to the current physical length of the actuator	
	result = adc.readADCSingleEnded(1)
	#map the result to the range 0->1
	result = (result - Actuator1FullInRaw) / (Actuator1FullOutRaw - Actuator1FullInRaw)
	#now map to the range fullIn -> fullOut
	result=result * (ActuatorFullOut - ActuatorFullIn) + ActuatorFullIn
	#result is now in mm's
	return result

def readActuator2():
	#reads the adc and maps the result to the current physical length of the actuator
	result = adc.readADCSingleEnded(2)
	#map the result to the range 0->1
	result = (result - Actuator2FullInRaw) / (Actuator2FullOutRaw - Actuator2FullInRaw)
	#now map to the range fullIn -> fullOut
	result=result * (ActuatorFullOut - ActuatorFullIn) + ActuatorFullIn
	#result is now in mm's
	return result
	
def sendSabertooth(address, command, speed):
	# sends commands to the sabertooth 
	checksum = int(address) + int(command) + int(speed) & 127
	#packet = ((chr(int(address))) + (chr(int(command))) + (chr(int(speed))) + (chr(int(checksum))))
	#print packet
	#controller.write(packet)
	controller.write(chr(int(address)))
	controller.write(chr(int(command)))
	controller.write(chr(int(speed)))
	controller.write(chr(int(checksum)))

def setActuators(actuator1, actuator2):
	#moves actuators independently
	leftSpeed = (actuator1 - 127)   # range is now -127 to 127
	rightSpeed = (actuator2 - 127) 
	
	#constrain the range of data sent to the sabertooth
	leftSpeed = max(leftSpeed, -127)
	leftSpeed = min(leftSpeed, 127)
	rightSpeed = max(rightSpeed, -127)
	rightSpeed = min(rightSpeed, 127)
	#print str(leftSpeed)
	#print str(rightSpeed)
	# send forward / reverse commands to controllers
	if(leftSpeed >= 0):
		sendSabertooth(address, 0, leftSpeed)
	else:
		sendSabertooth(address, 1, -1 * leftSpeed)
	
	if(rightSpeed >= 0):
		sendSabertooth(address, 5, rightSpeed)
	else:
		sendSabertooth(address, 4, -1 * rightSpeed)
	
def parseCommand(command): # Parses Socket Data back to Axis positions
	if len(command) > 3:
		if command[0] == "#": # is valid
			if command[1] == "A":
				if command[2] == "T":	# controls both actuators individually 
					speed1 = int(ord(command[3]))
					speed2 = int(ord(command[4]))
					setActuators(speed1, speed2)
				
				if command[2] == "B": # rotate base
					servoDriver.setServo(4,1696 + int(ord(command[3])) - 127)
				
				elif command[2] == "W": # rotate wrist joint up/down				
					wristTilt.setRelative(int(ord(command[3])))
				
				elif command[2] == "P": # pan gripper left/right					
					wristPan.setRelative(int(ord(command[3])))
				
				elif command[2] == "H": # twist gripper cw/ccw			
					wristTwist.setRelative(int(ord(command[3])))
				
				elif command[2] == "G": # open or close gripper
					temp = int(ord(command[3])) - 127
					#range of temp is now -127 to 127
					if temp >= 0:	#negative values correspond to the other trigger so ignore them
						temp = float(temp*800/127)
						#range of temp is now 0 to 800
						#right gripper:	
						#	open - 2000
						#	closed - 1200
						#left gripper:
						#	open - 1200
						#	closed - 2000
						#math for gripper position
						gripperRight = 2000 - int(temp)
						gripperLeft = int(temp) + 1200
						#update gripper position
						servoDriver.setServo(5, gripperLeft)
						servoDriver.setServo(6, gripperRight)
						
				elif command[2] == "K":  # turns off the arm 
					sendSabertooth(address,0, 0)
					sendSabertooth(address,4, 0)
					GPIO.output(16, False)
					print("Arm Off")
					servoDriver.reset()
				
				elif command[2] == "R":  # turns on the arm 
					GPIO.output(16, True)
					sendSabertooth(address,0, 0)
					sendSabertooth(address,5, 0)
					print("Arm On")

def stopSockets(): # Stops sockets on error condition
	try:
		armSocket.close()
	except:
		pass
	try:
		serverSocket.close()
	except:
		pass


### Main Program  ###

# set up ADC
#adc = ADS1x15(0x48)

# set up Sabertooth
controller = serial.Serial("/dev/ttyAMA0", bytesize = 8, parity = 'N', stopbits = 1)
controller.baudrate = 9600
controller.timeout = 0.2
sendSabertooth(address, 16, ramping)

# set up GPIOs
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.OUT)
GPIO.output(16, False)	# disconnect ArmPower

# set up servo driver
servoDriver = ServoDriver()
servoDriver.setServo(4,1696)
wristPan = Servo(servoDriver, 9, 830, 2350, 1600)
wristTilt = Servo(servoDriver, 8, 1000, 1700, 1370)
wristTwist = Servo(servoDriver, 7, 830, 2350, 1600)
servoDriver.setServo(5,1200)
servoDriver.setServo(6,2000)
	
# begin server connection
try:
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serverSocket.bind(("", armPort))
	serverSocket.listen(0)
	print("using serial port " + controller.name)
	print("ArmServer listening on port " + str(armPort))
	#main execution loop
	while(True):
		(armSocket, clientAddress) = serverSocket.accept()
		print("Connected to " + str(clientAddress[0]))
		while(True):
			data = armSocket.recv(256)
			if(data == ""): # socket closing
				sendSabertooth(address,0, 0)
				sendSabertooth(address,5, 0)
				break
			else:
				parseCommand(data)
		print("Connection to " + str(clientAddress[0]) + " was closed")
except KeyboardInterrupt:
	print("\nmanual shutdown...")
	sendSabertooth(address,0, 0)
	sendSabertooth(address,5, 0)
	GPIO.output(16,False)
	print("Arm Off")
	servoDriver.reset()
	stopSockets()
	GPIO.cleanup()
	raise
except socket.error as e:
	print(e.strerror)
	sendSabertooth(address,0, 0)
	sendSabertooth(address,5, 0)
	GPIO.output(16,False)
	print("Arm Off")
	servoDriver.reset()
	stopSockets()
	GPIO.cleanup()
	raise
except:
	print("error")
	sendSabertooth(address,0, 0)
	sendSabertooth(address,5, 0)
	GPIO.output(16,False)
	print("Arm Off")
	servoDriver.reset()
	stopSockets()
	GPIO.cleanup()
	raise
