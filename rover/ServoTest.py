from ServoDriver import *
import time

servoDriver = ServoDriver()

## Test Code
while True:
	pos1 = raw_input('Pulse Length Position: ')
	#pos2 = raw_input('Pulse Length Position?')
	
	try:
		servoDriver.setServo(8,int(pos1))
		#servoDriver.setServo(7,int(pos2))
	except:
		print("NaN!")
