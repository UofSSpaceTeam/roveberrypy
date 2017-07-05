from .RoverProcess import RoverProcess
from .GPSProcess import GPSPosition
from math import asin, atan2, cos, pi, radians, sin, sqrt, degrees, atan
import time
from statistics import mean
from .differential_drive_lib import diff_drive_fk, inverse_kinematics_drive

WHEEL_RADIUS = 14.5 # cm
MIN_WHEEL_RPM = 4.385095 # ERPM = 1000

ROVER_WIDTH = 1 # m

CALIBRATION_SAMPLES = 30

class NavigationProcess(RoverProcess):
	''' Aggregates data from GPS, Magnetometer, LIDAR, etc,
		and makes driving decisions based on the rover's
		surroundings.
	'''

	def setup(self, args):
		self.position = None
		self.position_last = None

		self.heading = None
		self.heading_last = None

		self.velocity = [0,0] # m/s, north, east
		self.accel = [0,0] #m/s^2, north, east

		self.bearing_error = 5 # TODO: What unit is this in?
		self._rotating = False

		self.finished_nav = True

		self.target = None
		self.target_reached_distance = 1  # metres
		self.target_maximum_distance = 10 # metres

		# Delay for loop in miliseconds
		self.loop_delay = 100

		# TODO: Why is this 2000, I found it in DriveProcess.py as min_rpm?
		self.motor_rpm = 2000
		self.right_rpm = 0 # wheel RPMs
		self.left_rpm = 0 # wheel RPMs
		self.right_speed = 0 # velocity of right wheel from axel
		self.left_speed = 0 # velocity of left wheel from axel

		self.starting_calibration_gps = [[],[]] # list of GPS positions that ar averaged
		self.starting_calibration_heading = []

		for msg in ["LidarDataMessage", "CompassDataMessage",
					"targetGPS", "singlePointGPS", "GPSVelocity",
					"updateLeftWheelRPM", "updateRightWheelRPM"
					]:
			self.subscribe(msg)

	def loop(self):
		time.sleep(self.loop_delay / 1000.0)

		if self.target is None:
			self.finished_nav = True

		if self.position is not None and not self.finished_nav:
			distance = self.position.distance(self.target)
			bearing = self.position.bearing(self.target)

			if distance < self.target_reached_distance:
				self.target = None
				self.publish("DriveStop")
				self.stopped = True

			if abs(bearing) < self.bearing_error and self._rotating:
				self.rotating = False
				self.publish("DriveForward", MIN_WHEEL_RPM)
				self.left_rpm = MIN_WHEEL_RPM
				self.right_rpm = MIN_WHEEL_RPM
			else:
				self.rotating = True
				if bearing < 0:
					self.publish("DriveRotateLeft", MIN_WHEEL_RPM)
					self.left_rpm = -MIN_WHEEL_RPM
					self.right_rpm = MIN_WHEEL_RPM
				else:
					self.publish("DriveRotateRight", MIN_WHEEL_RPM)
					self.left_rpm = MIN_WHEEL_RPM
					self.right_rpm = -MIN_WHEEL_RPM
			self.update_wheel_velocity()

	def update_wheel_velocity(self):
		self.right_speed = self.right_rpm*WHEEL_RADIUS/2
		self.left_speed = self.left_rpm*WHEEL_RADIUS/2

	def gps_g_h_filter(self, z, x0, dx, g, h, dt=1):
		x_est = x0
		#prediction step
		x_pred = x_est + atan((dx*dt)/GPSPosition.RADIUS)

		# update step
		residual = z - x_pred
		dx = dx    + h * (residual) / dt
		x_est  = x_pred + g * residual
		return x_est

	def vel_g_h_filter(self, z, x0, dx, g, h, dt=1):
		x_est = x0
		#prediction step
		x_pred = x_est + dt*dx

		# update step
		residual = z - x_pred
		dx = dx    + h * (residual) / dt
		x_est  = x_pred + g * residual
		return x_est

	def heading_g_h_filter(self, z, x0, dx, g, h, dt=1):
		x_est = x0
		#prediction step
		x_pred = x_est + dt*dx

		# update step
		residual = z - x_pred
		dx = dx    + h * (residual) / dt
		x_est  = x_pred + g * residual
		return x_est

	def on_LidarDataMessage(self, lidarmsg):
		''' LidarDataMessage contains:
			distance (centimeters): The lidar unit fires a laser
				beam directly forwards. When it hits an object,
				the length of this beam is the distance.
			angle (degrees): The angle at which the distance
				measurement was taken.
			tilt (degrees): virtical angle the distance was measured at.
		'''
		self.log("Dist: {} Angle: {} Tilt {}".format(lidarmsg.distance,
			lidarmsg.angle/100, lidarmsg.tilt))

	def on_CompassDataMessage(self, msg):
		''' CompassDataMessage contains:
			heading (degrees): Relative to north, the angle of
				rotation on the axis normal to the earth's surface.
			pitch (degrees):
			roll (degrees):
		'''
		tmp = time.time()
		d_t = tmp-self.last_compasmessage
		self.last_compasmessage = tmp
		self.log("heading: "+str(msg.heading))
		if self.heading is not None:
			self.heading_last = self.heading
			self.heading = self.heading_g_h_filter(msg.heading, self.heading,
					(self.right_speed-self.left_speed)/ROVER_WIDTH, 0.5, 0.05, d_t)
		else:
			if len(self.starting_calibration_heading) < CALIBRATION_SAMPLES:
				self.starting_calibration_heading.append(msg.heading)
			else:
				self.starting_calibration_heading.append(msg.heading)
				self.heading_last = self.heading
				self.heading = mean(self.starting_calibration_heading)

	def on_targetGPS(self, pos):
		'''Targets a new GPS coordinate'''
		target = GPSPosition(radians(pos[0]), radians(pos[1]))
		self.finished_nav = False

		if target.distance(self.position) <= self.maximum_target_distance:
			self.target = target

	def on_singlePointGPS(self, pos):
		'''Updates GPS position'''
		#std_dev 1.663596084712623e-05, 2.1743680968892167e-05
		# self.log("{},{}".format(degrees(pos.lat), degrees(pos.lon)))
		if self.position is not None:
			pos_pred_lat = self.gps_g_h_filter(pos.lat, self.position.lat, self.velocity[0], 0.25, 0.02, GPSProcess.LOOP_PERIOD)
			pos_pred_lon = self.gps_g_h_filter(pos.lon, self.position.lon, self.velocity[1], 0.25, 0.02, GPSProcess.LOOP_PERIOD)
			self.log("{},{}".format(degrees(pos_pred_lat), degrees(pos_pred_lon)))
			self.position_last = self.position
			self.position = GPSPosition(pos_pred_lat, pos_pred_lon)
		else:
			if len(self.starting_calibration_gps[0]) < CALIBRATION_SAMPLES:
				print(len(self.starting_calibration[0]))
				self.starting_calibration_gps[0].append(pos.lat)
				self.starting_calibration_gps[1].append(pos.lon)
			else:
				self.starting_calibration_gps[0].append(pos.lat)
				self.starting_calibration_gps[1].append(pos.lon)
				self.position = GPSPosition(mean(self.starting_calibration_gps[0]), mean(self.starting_calibration_gps[1]))
				print("Done GPS calibration")
				self.log("{},{}".format(degrees(pos.lat), degrees(pos.lon)))

	def on_GPSVelocity(self, vel):
		# std_dev 0.04679680341613995, 0.035958365746391524
		# self.log("{},{}".format(vel[0], vel[1]))
		self.velocity[0] = self.vel_g_h_filter(vel[0], self.velocity[0], self.accel[0], 0.4, 0.01, 0.3)
		self.velocity[1] = self.vel_g_h_filter(vel[1], self.velocity[1], self.accel[1], 0.4, 0.01, 0.3)

	def on_updateLeftWheelRPM(self, rpm):
		''' Drive process can manually overide wheel rpm'''
		self.left_rpm = rpm

	def on_updateRightWheelRPM(self, rpm):
		''' Drive process can manually overide wheel rpm'''
		self.right_rpm = rpm

	def on_AccelerometerMessage(self, accel):
		raise NotImplementedError()

