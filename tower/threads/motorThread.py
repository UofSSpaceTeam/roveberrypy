import threading
from Queue import Queue
import time
from enum import Enum
import RPi.GPIO as gpio
from unicodeConvert import convert

class Pins(Enum):
	motorA = 23
	motorB = 24
	servoPwm = 18
	
class ServoPositions(Enum):
	lowerBound = 3
	pressed = 5.75
	released = 7

class motorThread(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "motorThread"
		self.mailbox = Queue()
		self.setupGpio()
		self.setupMotor()
		self.setupServo()
		
	def run(self):
		while True:
			while not self.mailbox.empty():
				data = self.mailbox.get()
				print data
				if "towerAim" in data:
					self.rotate(data["towerAim"])
				elif "centerCameraButton" in data:
					self.pressButton()
			time.sleep(0.1)
	
	def getRotation(self):
	#File Name: rotation_sensor.py
	#Project: USST Rover 2015
	#Coder(s): Ghazi Sami
	#Date Written: 5/11/2015
	#Description: This code is designed to obtain the output of the EMS22A Rotation Sensor
	#As a Base-10 number between 0 and 1023. The output is continually updated as the rotation changes.

		#Set pin numbering mode
		GPIO.setmode(GPIO.BCM)

		#Initialize pins:

		#Set Digital Input (Pin 1 on Sensor) to GND
		GPIO.setup(11, GPIO.OUT)  #Set clock pin (#2 on sensor) as an output
		#Set Pin #3 to GND
		GPIO.setup(7, GPIO.IN) #Set Digital Output (#4 on sensor) as an input
		#Set Pin #5 to VCC
		GPIO.setup(9, GPIO.OUT)  #Set chip select pin (#6 on sensor) as an output

		#Set initial values for clock and chip select:
		GPIO.output(11, True) 
		GPIO.output(9, False) 

		#Chip select must be high for a min of 500ns between readings
		GPIO.output(9, True)
		GPIO.output(9, False)

		#Initialize position output to 0:
		rotation = 0 ;

		#Read data from clock
		for x in range(0,9):
			#Have clock switch between high and low
			GPIO.output(11, False)
			GPIO.output(11, True)

		#Read data from pin
		if GPIO.input(7) == True:
			 b = 1
		else:
			 b = 0
		rotation = rotation + b * pow(2, 10-(x+1))

		#Run clock again for 7 iterations to allow for lag
		for x in range(0,6):
			GPIO.output(11,False)
			GPIO.output(11,True)
		return rotation
	
	def rotate(self, rotation):
		if self.getRotation() < rotation:
			initialTime = time.time()
			self.spinMotorLeft()
			while self.getRotation() < rotation:
				if time.time() - initialTime > 2:
					break
				time.sleep(0.01)
		if self.getRotation() > rotation:
			initialTime = time.time()
			self.spinMotorRight()
			while self.getRotation() > rotation:
				if time.time() - initialTime > 2:
					break
				time.sleep(0.01)
		self.stopMotor()
	
	def spinMotorLeft(self):
		gpio.output(Pins.motorA, 0)
		gpio.output(Pins.motorB, 1)
	
	def spinMotorRight(self):
		gpio.output(Pins.motorA, 1)
		gpio.output(Pins.motorB, 0)
	
	def stopMotor(self):
		gpio.output(Pins.motorA, 0)
		gpio.output(Pins.motorB, 0)

	def pressButton(self):
		self.activateServo()
		self.servo.ChangeDutyCycle(ServoPositions.pressed)
		time.sleep(0.3)
		self.servo.ChangeDutyCycle(ServoPositions.released)
		time.sleep(0.2)
		self.deactivateServo()
	
	def setupGpio(self):
		gpio.setmode(gpio.BCM)
		gpio.setwarnings(False)
	
	def setupServo(self):
		self.activateServo()
		self.servo = gpio.PWM(Pins.servoPwm, 50)
		self.servo.start(ServoPositions.lowerBound)
		self.servo.ChangeDutyCycle(ServoPositions.released)
		time.sleep(0.5)
		self.deactivateServo()
	
	def activateServo(self):
		gpio.setup(Pins.servoPwm, gpio.OUT)
	
	def deactivateServo(self):
		gpio.setup(Pins.servoPwm, gpio.IN)
	
	def setupMotor(self):
		gpio.setup(Pins.motorA, gpio.OUT)
		gpio.setup(Pins.motorB, gpio.OUT)
		self.stopMotor()
