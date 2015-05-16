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
		return 0
	
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
