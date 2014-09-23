	from ServoDriver import *
	import time
	
	experpos = 1700 # position to drop soil into experiment chamber
	samppos = 2100 # position to drop soil into sample chamber
	shakenum = 6 # number of times to "shake" servo before moving on
	shakeammount = 50 
	
	#setup servo
	servoDriver = ServoDriver()
	
	#move to position to drop soil into experiment chamber
	servoDriver.setServo(4,experpos)
	
	time.sleep(0.5)
	
	# "shake" servo to get more soil in 
	for i in range(0,shakenum)
		servoDriver.setservo(4, experpos + shakeammount)
		time.sleep(0.1)
		servoDriver.setservo(4, experpos - 2*shakeammount)
		time.sleep(0.1)
		servoDriver.setservo(4, experpos + 2*shakeammount)
		time.sleep(0.2)