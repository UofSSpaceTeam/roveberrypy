from .RoverProcess import RoverProcess
from .GPSProcess import GPSPosition, LOOP_PERIOD
from math import asin, atan2, cos, pi, radians, sin, sqrt, degrees, atan
import time
from statistics import mean
from .differential_drive_lib import diff_drive_fk, inverse_kinematics_drive

WHEEL_RADIUS = 14.5 # cm
MIN_WHEEL_RPM = 4.385095 # ERPM = 1000

ROVER_WIDTH = 1.2 # m

CALIBRATION_SAMPLES = 10

class NavigationProcess(RoverProcess):
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

		self.bearing_error = 5 # TODO: What unit is this in?
		self._rotating = False

		self.autonomous_mode = False
		self.state = "waiting" #can be "waiting" "driving" or "manual"

		# number of samples in our running average
		self.pos_samples = 1
		self.vel_samples = 1
		self.heading_samples = 1

		self.target = None
		self.target_reached_distance = 3  # metres
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
					"updateLeftWheelRPM", "updateRightWheelRPM",
					"AccelerometerMessage", "buttonA_down", "buttonB_down"
					]:
			self.subscribe(msg)

	def loop(self):
		time.sleep(self.loop_delay / 1000.0)

		if self.state == "waiting":
			self.wait_state()
		elif self.state == "driving":
			self.drive_state()
		elif self.state == "manual":
			pass # don't do anything in manual control mode
		else:
			self.log("Navigation in invalid state, reverting to wating...", "WARNING")
			self.state = "waiting"

		self.update_wheel_velocity()

	def drive_state(self):
		''' Function for handling drive state'''
		if self.position is not None:
			distance = self.position.distance(self.target)
			bearing = self.position.bearing(self.target)

			if abs(bearing) > self.bearing_error:
				if bearing < 0:
					self.publish("DriveRotateLeft", MIN_WHEEL_RPM)
					self.left_rpm = -MIN_WHEEL_RPM
					self.right_rpm = MIN_WHEEL_RPM
				else:
					self.publish("DriveRotateRight", MIN_WHEEL_RPM)
					self.left_rpm = MIN_WHEEL_RPM
					self.right_rpm = -MIN_WHEEL_RPM
				return # back to loop
			elif distance > self.target_reached_distance:
				self.publish("DriveForward", MIN_WHEEL_RPM)
				self.left_rpm = MIN_WHEEL_RPM
				self.right_rpm = MIN_WHEEL_RPM
				return #back to loop
			else:
				self.target = None
				self.publish("TargetReached")
				self.state = "waiting"

	def wait_state(self):
		''' Function for handling waiting state'''
		self.publish("DriveStop", 0)

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
		return x_est, dx

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
		self.log("heading: "+str(msg.heading))
		if self.heading is not None:
			self.heading_last = self.heading
			if self.state == "waiting":
				self.heading = (self.heading + msg.heading)/(self.heading_samples)
				self.heading_samples += 1
			else:
				tmp = time.time()
				d_t = tmp-self.last_compassmessage
				self.last_compassmessage = tmp
				self.heading = self.g_h_filter(msg.heading, self.heading,
						(self.right_speed-self.left_speed)/ROVER_WIDTH, 0.5, 0.05, d_t)
				self.publish("RoverHeading", self.heading)
		else:
			if len(self.starting_calibration_heading) < CALIBRATION_SAMPLES:
				# Keep averaging
				self.starting_calibration_heading.append(msg.heading)
			else:
				# 'calibration' done
				self.starting_calibration_heading.append(msg.heading)
				self.heading_last = self.heading
				self.heading = mean(self.starting_calibration_heading)

	def on_targetGPS(self, pos):
		'''Targets a new GPS coordinate'''
		target = GPSPosition(radians(pos[0]), radians(pos[1]))
		if target.distance(self.position) <= self.maximum_target_distance:
			self.target = target
			if self.state != "manual":
				self.state = "driving"

	def on_singlePointGPS(self, pos):
		'''Updates GPS position'''
		#std_dev 1.663596084712623e-05, 2.1743680968892167e-05
		# self.log("{},{}".format(degrees(pos.lat), degrees(pos.lon)))
		if self.state == "waiting" and self.position is not None:
			lat = (self.position.lat + pos.lat)/(self.pos_samples)
			lon = (self.position.lon + pos.lon)/(self.pos_samples)
			self.pos_samples += 1
			# self.position = GPSPosition(lat, lon)
			self.log("{},{}".format(degrees(self.position.lat), degrees(self.position.lon)), "DEBUG")
			self.publish("RoverPosition", [degrees(self.position.lat), degrees(self.position.lon)])
			return
		if self.position is not None:
			k = 0.0 # determens which to trust more; velocity(0), or wheels (1)
			pos_pred_lat_vel = self.pos_g_h_filter_vel(pos.lat,
					self.position.lat, self.velocity[0], 0.25, LOOP_PERIOD)
			pos_pred_lon_vel = self.pos_g_h_filter_vel(pos.lon,
					self.position.lon, self.velocity[1], 0.25, LOOP_PERIOD)

			fk_pred = diff_drive_fk(0,0, ROVER_WIDTH, self.heading, self.left_speed, self.right_speed, LOOP_PERIOD)
			pos_pred_lat_wheel = self.pos_g_h_filter_wheel(pos.lon, self.position.lat, fk_pred[0], 0.3, LOOP_PERIOD)
			pos_pred_lon_wheel = self.pos_g_h_filter_wheel(pos.lon, self.position.lon, fk_pred[1], 0.3, LOOP_PERIOD)
			pos_pred_lat = pos_pred_lat_vel*(1-k) + pos_pred_lat_wheel*k
			pos_pred_lon = pos_pred_lon_vel*(1-k) + pos_pred_lon_wheel*k
			self.log("{},{}".format(degrees(pos_pred_lat), degrees(pos_pred_lon)), "DEBUG")
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
				self.log("{},{}".format(degrees(pos.lat), degrees(pos.lon)), "DEBUG")

	def on_GPSVelocity(self, vel):
		# std_dev 0.04679680341613995, 0.035958365746391524
		# self.log("{},{}".format(vel[0], vel[1]))
		if self.state == "waiting":
			self.velocity[0] = (self.velocity[0] + vel[0])/(self.vel_samples)
			self.velocity[1] = (self.velocity[1] + vel[1])/(self.vel_samples)
			self.vel_samples += 1
		else:
			k = 0.0 #constant determining which to trust more; acceleration(0) or wheels(1)
			v_acc_x = self.g_h_filter(vel[0], self.velocity[0], self.accel[0], 0.4, LOOP_PERIOD)
			v_acc_y = self.g_h_filter(vel[1], self.velocity[1], self.accel[1], 0.4, LOOP_PERIOD)

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
		self.log("x: {}, y: {}, z: {}".format(accel.x, accel.y, accel.z))
		self.accel[0] = accel.x
		self.accel[1] = accel.y

	def on_ButtonA_down(self, data):
		self.state = "waiting"

	def on_ButtonB_down(sel, data):
		self.state = "manual"

