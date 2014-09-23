from LSM303 import LSM303
from ServoDriver import *

currentYaw = 1600

compass = LSM303(busnum = 0)
servoDriver = ServoDriver()
servoDriver.setServo(4, currentYaw)
print "Antenna bearing is " + str(round((compass.read() + 180) % 360))

while True:
	input = raw_input('Enter r to turn right, l to turn left or c to read compass: ')
	if input == "l":
		currentYaw += 15
		if currentYaw > 2300:
			currentYaw = 2300
		servoDriver.setServo(4, currentYaw)
	elif input == "r":
		currentYaw -= 15
		if currentYaw < 1000:
			currentYaw = 1000
		servoDriver.setServo(4, currentYaw)
	elif input == "c":
		print "Antenna bearing is " + str(round((compass.read() + 180) % 360))
	