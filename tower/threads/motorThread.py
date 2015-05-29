import threading
from Queue import Queue
import time
from enum import Enum
import RPi.GPIO as gpio
from unicodeConvert import convert

class Pins(Enum):
	motorA = 17
	motorB = 24 
	servoPwm = 18
	sensorClock = 11
	sensorChipSelect = 9
	sensorOutput = 7
	
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
		self.setupSensor()
		self.calibrate = 0
		
	def run(self):
		while True:
			while not self.mailbox.empty():
				data = self.mailbox.get()
				print data
				if "towerAim" in data:
					self.rotate(data["towerAim"])
				if "calibrate" in data:
					#self.calibrate = 0.0 
					self.calibrate = self.getRotation()
					print self.calibrate
				if "towerJog" in data:
					self.jog(data["towerJog"])
				elif "centerCameraButton" in data:
					self.pressButton()
			time.sleep(0.1)
	
	def getRotation(self):
		rotation = 0x0000
		gpio.output(Pins.sensorChipSelect, 0)
		# clock in data
		s = ""
		for i in range(0, 9):
			gpio.output(Pins.sensorClock, 0)
			gpio.output(Pins.sensorClock, 1)
			if gpio.input(Pins.sensorOutput):
				s += "1"
				rotation += 2**(10-(i+1))
			else:
				s += "0"
		for i in range(9, 15):
			gpio.output(Pins.sensorClock, 0)
			gpio.output(Pins.sensorClock, 1)
		gpio.output(Pins.sensorChipSelect, 1)
		time.sleep(0.001)
#		rotation = (rotation-336)*(360/1023.0)
		rotation = (rotation)/8.5-self.calibrate
		print rotation
		print s
		return rotation
	
	def rotate(self, rotation):
		if self.getRotation() < rotation:
			initialTime = time.time()
			self.spinMotorLeft(rotation)
			while self.getRotation() < rotation:
				if time.time() - initialTime > 2:
					break
				time.sleep(0.01)
		if self.getRotation() > rotation:
			initialTime = time.time()
			self.spinMotorRight(rotation)
			while self.getRotation() > rotation:
				if time.time() - initialTime > 2:
					break
				time.sleep(0.01)
		self.stopMotor()
	
	def jog(self, direction):
		if direction == "L":
			slight_left = self.getRotation() + 10
			self.spinMotorLeft(slight_left)
		elif direction == "R":
			slight_right = self.getRotation() - 10
			self.spinMotorRight(slight_right)
		time.sleep(0.2)
		try:
			self.getRotation()
			self.getRotation()
			self.getRotation()
			self.getRotation()
			self.getRotation()
		finally:
			self.stopMotor()
	
	def spinMotorLeft(self, rotation):
		initialTime = time.time()
		initialRotation = self.getRotation()
		gpio.output(Pins.motorA, 0)
		while self.getRotation() < rotation:
			gpio.output(Pins.motorB, 1)
			time.sleep(0.01)
			gpio.output(Pins.motorB, 0)
			time.sleep(0.04)
			if time.time() - initialTime > 1:
				if abs(self.getRotation() - initialRotation) < 1:
					print "Warning: No Movement"
				break
	
	def spinMotorRight(self, rotation):
		initialTime = time.time()
		initialRotation = self.getRotation()
		gpio.output(Pins.motorB, 0)
		while self.getRotation() > rotation:
			gpio.output(Pins.motorA, 1)
			time.sleep(0.01)
			gpio.output(Pins.motorA, 0)
			time.sleep(0.04)
			if time.time() - initialTime > 1:
				if abs(self.getRotation() - initialRotation) < 1:
					print "Warning: No Movement"
				break
	
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
	
	def setupSensor(self):
		gpio.setup(Pins.sensorClock, gpio.OUT)
		gpio.setup(Pins.sensorOutput, gpio.IN)
		gpio.setup(Pins.sensorChipSelect, gpio.OUT)
		# Set initial values for clock and chip select:
		gpio.output(Pins.sensorClock, 1) 
		gpio.output(Pins.sensorChipSelect, 1) 

