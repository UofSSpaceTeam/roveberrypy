import smbus
import math
import time

class Servo:
	def __init__(self, driver, channel, minimum, maximum, default, debug=False):
		self.driver = driver
		self.channel = channel
		if maximum > minimum:
			self.minimum = minimum
			self.maximum = maximum
		else:
			self.minimum = maximum
			self.maximum = minimum
		self.default = default
		self.currentPosition = default
		self.driver.setServo(self.channel, int(default))
	
	def setRelative(self, change):
		self.currentPosition += (change - 127)
		self.currentPosition = max(self.currentPosition, self.minimum)
		self.currentPosition = min(self.currentPosition, self.maximum)
		self.driver.setServo(self.channel, int(self.currentPosition))
	
	def setMicroseconds(self, micros):
		self.currentPosition = max(micros, self.minimum)
		self.currentPosition = min(self.currentPosition, self.maximum)
		self.driver.setServo(self.channel, int(self.currentPosition))

class ServoDriver:
	# communication constants
	__SUBADR1            = 0x02
	__SUBADR2            = 0x03
	__SUBADR3            = 0x04
	__MODE1              = 0x00
	__PRESCALE           = 0xFE
	__LED0_ON_L          = 0x06
	__LED0_ON_H          = 0x07
	__LED0_OFF_L         = 0x08
	__LED0_OFF_H         = 0x09
	__ALLLED_ON_L        = 0xFA
	__ALLLED_ON_H        = 0xFB
	__ALLLED_OFF_L       = 0xFC
	__ALLLED_OFF_H       = 0xFD
	
	def __init__(self):
		self.i2c = I2C()
		self.reset()
	
	def reset(self):
		self.i2c.write(self.__MODE1, 0x00)
		time.sleep(0.05)
		oldmode = self.i2c.read(self.__MODE1);
		newmode = (oldmode & 0x7F) | 0x10
		self.i2c.write(self.__MODE1, newmode)
		self.i2c.write(self.__PRESCALE, 100) # decrease for higher frequency
		self.i2c.write(self.__MODE1, oldmode)
		time.sleep(0.005)
		self.i2c.write(self.__MODE1, oldmode | 0x80)
	
	def setServo(self, channel, pulse):
		if(channel >= 0 and channel <= 15):
			#print("ch" + str(channel) + ": " + str(pulse))
			tick = int(pulse / 4.069)
			self.i2c.write(self.__LED0_ON_L+4*channel, 0x00)
			self.i2c.write(self.__LED0_ON_H+4*channel, 0x00)
			self.i2c.write(self.__LED0_OFF_L+4*channel, tick & 0xFF)
			self.i2c.write(self.__LED0_OFF_H+4*channel, tick >> 8)
		else:
			print("invalid servo channel")	


class I2C:
	def __init__(self):
		self.bus = smbus.SMBus(1)
	
	def write(self, reg, value):
		try:
			self.bus.write_byte_data(0x40, reg, value)
		except IOError, err:
			print "Error accessing servo board at 0x40: Check your I2C"

	def read(self, reg):
		try:
			result = self.bus.read_byte_data(0x40, reg)
			return result
		except IOError, err:
			print "Error accessing servo board at 0x40: Check your I2C"
			return None

