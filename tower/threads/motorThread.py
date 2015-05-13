import threading
from Queue import Queue
import time
import RPi.GPIO as gpio
from unicodeConvert import convert

class motorThread(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "motorThread"
		self.mailbox = Queue()
		gpio.setmode(gpio.BCM)
		gpio.setwarnings(False)
		gpio.setup(23, gpio.OUT) # motor A
		gpio.setup(24, gpio.OUT) # motor B
		gpio.setup(18, gpio.OUT) # servo
		self.servo = gpio.PWM(18, 50)
		self.servo.start(3.0)
		self.servo.ChangeDutyCycle(6)
		gpio.setup(18, gpio.IN)
		
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
	
	def rotate(self, position):
		print "moving to: " + str(position)

	def pressButton(self):
		print "pushing button"
		gpio.setup(18, gpio.OUT) # servo
		self.servo.ChangeDutyCycle(10)
		time.sleep(0.5)
		self.servo.ChangeDutyCycle(6)
		time.sleep(0.5)
		gpio.setup(18, gpio.IN)
		

