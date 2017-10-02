from .RoverProcess import RoverProcess
from .GPSProcess import GPSPosition, LOOP_PERIOD
from math import asin, atan2, cos, pi, radians, sin, sqrt, degrees, atan
import time
from statistics import mean
from .differential_drive_lib import diff_drive_fk
import json
import math

WHEEL_RADIUS = 14.5 # cm
MIN_WHEEL_RPM = 4.385095 # ERPM = 1000

ROVER_WIDTH = 1.2 # m

CALIBRATION_SAMPLES = 10

class SimpleNavigationProcess(RoverProcess):
	''' Aggregates data from GPS, Magnetometer, LIDAR, etc,
		and makes driving decisions based on the rover's
		surroundings.
	'''

	def setup(self, args):
		self.position = None
		self.position_last = None

		self.heading = 0
		self.heading_last = 0

		self.velocity = [0,0] # m/s, north, east
		self.accel = [0,0] #m/s^2, north, east


		self.last_compassmessage = 0

		# Delay for loop in miliseconds
		self.loop_delay = 100

		# TODO: Why is this 2000, I found it in DriveProcess.py as min_rpm?
		self.right_rpm = 0 # wheel RPMs
		self.left_rpm = 0 # wheel RPMs
		self.right_speed = 0 # velocity of right wheel from axel
		self.left_speed = 0 # velocity of left wheel from axel

		self.starting_calibration_gps = [[],[]] # list of GPS positions that ar averaged
		self.starting_calibration_heading = []

		for msg in ["LidarDataMessage", "CompassDataMessage",
					"singlePointGPS", "GPSVelocity",
					"updateLeftWheelRPM", "updateRightWheelRPM",
					"AccelerometerMessage",
					]:
			self.subscribe(msg)

	def loop(self):
		time.sleep(self.loop_delay / 1000.0)

		self.update_wheel_velocity()

	def update_wheel_velocity(self):
		self.right_speed = self.right_rpm*WHEEL_RADIUS/2
		self.left_speed = self.left_rpm*WHEEL_RADIUS/2

	def pos_g_h_filter_vel(self, z, x0, dx, g, dt=1):
		x_est = x0
		#prediction step
		x_pred = x_est + atan((dx*dt)/GPSPosition.RADIUS)

		# update step
		residual = z - x_pred
		x_est  = x_pred + g * residual
		return x_est

	def pos_g_h_filter_wheel(self, z, x0, dx, g, dt=1):
		x_est = x0
		#prediction step
		x_pred = x_est + atan((dx)/GPSPosition.RADIUS)

		# update step
		residual = z - x_pred
		x_est  = x_pred + g * residual
		return x_est

	def g_h_filter(self, z, x0, dx, g, dt=1):
		x_est = x0
		#prediction step
		x_pred = x_est + dt*dx

		# update step
		residual = z - x_pred
		x_est  = x_pred + g * residual
		return x_est

	def on_CompassDataMessage(self, msg):
		''' CompassDataMessage contains:
			heading (degrees): Relative to north, the angle of
				rotation on the axis normal to the earth's surface.
			pitch (degrees):
			roll (degrees):
		'''
		if self.heading is not None:
			self.heading_last = self.heading
			tmp = time.time()
			d_t = tmp-self.last_compassmessage
			self.last_compassmessage = tmp
			self.heading = self.g_h_filter(msg.heading, self.heading,
					(self.right_speed-self.left_speed)/ROVER_WIDTH, 0.8, d_t)
			self.publish("RoverHeading", self.heading)
			# self.log("heading: {}".format(self.heading))

	def on_singlePointGPS(self, pos):
		'''Updates GPS position'''
		#std_dev 1.663596084712623e-05, 2.1743680968892167e-05
		# self.log("{},{}".format(degrees(pos.lat), degrees(pos.lon)))
		if self.position is not None:
			k = 0.0 # determens which to trust more; velocity(0), or wheels (1)
			pos_pred_lat_vel = self.pos_g_h_filter_vel(pos.lat,
					self.position.lat, self.velocity[0], 0.1, LOOP_PERIOD)
			pos_pred_lon_vel = self.pos_g_h_filter_vel(pos.lon,
					self.position.lon, self.velocity[1], 0.1, LOOP_PERIOD)

			fk_pred = diff_drive_fk(0,0, ROVER_WIDTH, self.heading, self.left_speed, self.right_speed, LOOP_PERIOD)
			pos_pred_lat_wheel = self.pos_g_h_filter_wheel(pos.lon, self.position.lat, fk_pred[0], 0.3, LOOP_PERIOD)
			pos_pred_lon_wheel = self.pos_g_h_filter_wheel(pos.lon, self.position.lon, fk_pred[1], 0.3, LOOP_PERIOD)
			pos_pred_lat = pos_pred_lat_vel*(1-k) + pos_pred_lat_wheel*k
			pos_pred_lon = pos_pred_lon_vel*(1-k) + pos_pred_lon_wheel*k
			self.log("{},{},{}".format(time.time(), degrees(pos_pred_lat), degrees(pos_pred_lon)), "INFO")
			self.position_last = self.position
			self.position = GPSPosition(pos_pred_lat, pos_pred_lon)
			self.publish("RoverPosition", [degrees(pos_pred_lat), degrees(pos_pred_lon)])
		else:
			if len(self.starting_calibration_gps[0]) < CALIBRATION_SAMPLES:
				self.starting_calibration_gps[0].append(pos.lat)
				self.starting_calibration_gps[1].append(pos.lon)
			else:
				# Done averaging
				self.starting_calibration_gps[0].append(pos.lat)
				self.starting_calibration_gps[1].append(pos.lon)
				self.position = GPSPosition(mean(self.starting_calibration_gps[0]), mean(self.starting_calibration_gps[1]))
				self.log("{},{},{}".format(time.time(),degrees(pos.lat), degrees(pos.lon)), "INFO")

	def on_GPSVelocity(self, vel):
		# std_dev 0.04679680341613995, 0.035958365746391524
		# self.log("{},{}".format(vel[0], vel[1]))
		k = 0.1 #constant determining which to trust more; acceleration(0) or wheels(1)
		v_acc_x = self.g_h_filter(vel[0], self.velocity[0], self.accel[0], 0.2, LOOP_PERIOD)
		v_acc_y = self.g_h_filter(vel[1], self.velocity[1], self.accel[1], 0.2, LOOP_PERIOD)

		v_wheel_x = self.g_h_filter(vel[0], self.velocity[0], 0.4, LOOP_PERIOD)
		v_wheel_y = self.g_h_filter(vel[1], self.velocity[1], 0.4, LOOP_PERIOD)

		self.velocity[0] = v_acc_x*(1-k) + v_wheel_x*k

	def on_updateLeftWheelRPM(self, rpm):
		''' Drive process can manually overide wheel rpm'''
		self.left_rpm = rpm

	def on_updateRightWheelRPM(self, rpm):
		''' Drive process can manually overide wheel rpm'''
		self.right_rpm = rpm

	def on_AccelerometerMessage(self, accel):
		#mean when stationary: 0.07603603603603604, 0.6156756756756757
		k = 0.2 # trust factor in our acceleration readings
		stationary_accel = (0.07603603603603604, 0.6156756756756757)
		self.accel[0] = k*(accel.x - stationary_accel[0])
		self.accel[1] = k*(accel.y - stationary_accel[1])
		# self.log("{},{}".format(self.accel[0], self.accel[1]))

