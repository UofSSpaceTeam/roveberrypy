from Adafruit_I2C import Adafruit_I2C
import math

class LSM303():

	# Minimal constants carried over from Arduino library
	LSM303_ADDRESS_ACCEL = (0x30 >> 1)  # 0011001x
	LSM303_ADDRESS_MAG   = (0x3C >> 1)  # 0011110x
											 # Default	Type
	LSM303_REGISTER_ACCEL_CTRL_REG1_A = 0x20 # 00000111   rw
	LSM303_REGISTER_ACCEL_CTRL_REG4_A = 0x23 # 00000000   rw
	LSM303_REGISTER_ACCEL_OUT_X_L_A   = 0x28
	LSM303_REGISTER_MAG_CRB_REG_M	 = 0x01
	LSM303_REGISTER_MAG_MR_REG_M	  = 0x02
	LSM303_REGISTER_MAG_OUT_X_H_M	 = 0x03

	# Gain settings for setMagGain()
	LSM303_MAGGAIN_1_3 = 0x20 # +/- 1.3
	LSM303_MAGGAIN_1_9 = 0x40 # +/- 1.9
	LSM303_MAGGAIN_2_5 = 0x60 # +/- 2.5
	LSM303_MAGGAIN_4_0 = 0x80 # +/- 4.0
	LSM303_MAGGAIN_4_7 = 0xA0 # +/- 4.7
	LSM303_MAGGAIN_5_6 = 0xC0 # +/- 5.6
	LSM303_MAGGAIN_8_1 = 0xE0 # +/- 8.1
	

	def __init__(self, busnum=-1, debug=False, hires=False):

		# Accelerometer and magnetometer are at different I2C
		# addresses, so invoke a separate I2C instance for each
		self.accel = Adafruit_I2C(self.LSM303_ADDRESS_ACCEL, busnum, debug)
		self.mag   = Adafruit_I2C(self.LSM303_ADDRESS_MAG  , busnum, debug)

		# Enable the accelerometer
		self.accel.write8(self.LSM303_REGISTER_ACCEL_CTRL_REG1_A, 0x27)
		# Select hi-res (12-bit) or low-res (10-bit) output mode.
		# Low-res mode uses less power and sustains a higher update rate,
		# output is padded to compatible 12-bit units.
		if hires:
			self.accel.write8(self.LSM303_REGISTER_ACCEL_CTRL_REG4_A,
			  0b00001000)
		else:
			self.accel.write8(self.LSM303_REGISTER_ACCEL_CTRL_REG4_A, 0)
  
		# Enable the magnetometer
		self.mag.write8(self.LSM303_REGISTER_MAG_MR_REG_M, 0x00)
		
		self.magMin = [-817, -1142, -623]
		self.magMax = [513, 503, 412]
		self.magAvg = [0, 0, 0]
		for i in range(0, 3):
			self.magAvg[i] = (self.magMax[i] + self.magMin[i]) / 2

	# Interpret signed 12-bit acceleration component from list
	def accel12(self, list, idx):
		n = list[idx] | (list[idx+1] << 8) # Low, high bytes
		if n > 32767: n -= 65536		   # 2's complement signed
		return n >> 4					  # 12-bit resolution


	# Interpret signed 16-bit magnetometer component from list
	def mag16(self, list, idx):
		n = (list[idx] << 8) | list[idx+1]   # High, low bytes
		return n if n < 32768 else n - 65536 # 2's complement signed


	def read(self):
		# Read the accelerometer
		list = self.accel.readList(self.LSM303_REGISTER_ACCEL_OUT_X_L_A | 0x80, 6)
		acc = (self.accel12(list, 0), self.accel12(list, 2), self.accel12(list, 4))
		# Read the magnetometer
		list = self.mag.readList(self.LSM303_REGISTER_MAG_OUT_X_H_M, 6)
		mag = [self.mag16(list, 0), self.mag16(list, 2), self.mag16(list, 4)]
		# calibration
		# for i in range(0, 3):
			# if(mag[i] < self.magMin[i]):
				# self.magMin[i] = mag[i]
			# if(mag[i] > self.magMax[i]):
				# self.magMax[i] = mag[i]
		mag[0] -= self.magAvg[0]
		mag[1] -= self.magAvg[1]
		mag[2] -= self.magAvg[2]
		# compute heading
		return self.heading(acc, mag)
	
	def heading(self, acc, mag):
		east = self.crossProduct(mag, acc)
		east = self.normalize(east)
		north = self.crossProduct(acc, east)
		north = self.normalize(north)
		heading = math.atan2(self.dotProduct(east, (0, -1, 0)), self.dotProduct(north, (0, -1, 0))) * 180 / math.pi
		if heading < 0:
			heading += 360
		return heading
	
	def crossProduct(self, a, b):
		x = a[1] * b[2] - a[2] * b[1]
		y = a[2] * b[0] - a[0] * b[2]
		z = a[0] * b[1] - a[1] * b[0]
		return (x, y, z)
	
	def dotProduct(self, a, b):
		x = a[0] * b[0]
		y = a[1] * b[1]
		z = a[2] * b[2]
		return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
	
	def normalize(self, a):
		mag = self.dotProduct(a, a) ** 0.5
		x = a[0] / mag
		y = a[1] / mag
		z = a[2] / mag
		return (x, y, z)
		
	def setMagGain(gain=LSM303_MAGGAIN_1_3):
		self.mag.write8( LSM303_REGISTER_MAG_CRB_REG_M, gain)


# calibration routine
	# from time import sleep

	# lsm = LSM303()
	# try:
		# while True:
			# lsm.read()
	# except KeyboardInterrupt:
		# for i in range(0, 3):
			# print("max " + str(i) + " = " + str(lsm.magMax[i]))
			# print("min " + str(i) + " = " + str(lsm.magMin[i]))
		# raise

