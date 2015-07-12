from towerprocess import TowerProcess

# your imports go here. For example:
import time
import RPi.GPIO as gpio

class ExampleProcess(RoverProcess):
	
	# helper classes go here if you want any
	class Pins(Enum):
		motorA = 17
		motorB = 24
		sensorClock = 11
		sensorChipSelect = 9
		sensorOutput = 7
		servoPwm = 18

	class ServoPositions(Enum):
		lowerBound = 3
		pressd = 5.75
		released = 7

	def setup(self, args):
		# your setup code here. examples:
		# self.something = args["something"]
		self.setupGpio()
		self.setupMotor()
		self.setupSensor()
		self.setupServo()
		self.calibrate = 0
	
	def loop(self):
		# your looping code here. for example:	


	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "calibrate" in message:
			self.calibrate = self.getRotation()
		if "towerJog" in message:
			self.jog(message["towerJog"])
		if "centerCameraButton" in message:
			self.pressButton()
	
	def cleanup(self):
		self.stopMotor()
		# your cleanup code here. e.g. stopAllMotors()
	
	# additional functions go here
	def setupGpio(self):
		gpio.setmode(gpio.BCM)
		gpio.setwarnings(False)
	
	def setupMotor(self):
		gpio.setup(Pins.motorA, gpio.OUT)
		gpio.setup(Pins.motorB, gpio.OUT)
		self.stopMotor()

	def setupSensor(self):
		gpio.setup(Pins.sensorClock, gpio.OUT)
		gpio.setup(Pins.sensorOutput, gpio.IN)
		gpio.setup(Pins.sensorChipSelect, gpio.OUT)
		#Set initial values for clock and chip select
		gpio.output(Pins.sensorClock, 1)
		gpio.output(Pins.sensorChipSelect, 1)

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

	def pressButton(self):
		self.activateServo()
		self.servo.ChangeDutyCycle(ServoPositions.pressed)
		time.sleep(0.3)
		self.servo.ChangeDutyCycle(ServoPositions.released)
		time.sleep(0.2)
		self.deactivateServo()

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
		finally:
			self.stopMotor()	

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
		rotation = (rotation)/8.0-self.calibrate
		return rotation

	def stopMotor(self):
		gpio.output(Pins.motorA, 0)
		gpio.output(Pins.motorB, 0)

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
