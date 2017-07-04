from .RoverProcess import RoverProcess
from .GPSProcess import GPSPosition
from math import asin, atan2, cos, pi, radians, sin, sqrt, degrees
import time

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

		self.bearing_error = 360 # TODO: What unit is this in?
		self._rotating = False

		self.target = None
		self.target_reached_distance = 1  # metres
		self.target_maximum_distance = 10 # metres

		# Delay for loop in miliseconds
		self.loop_delay = 100

		# TODO: Why is this 2000, I found it in DriveProcess.py as min_rpm?
		self.motor_rpm = 2000

		for msg in ["LidarDataMessage", "CompassDataMessage",
					"targetGPS", "singlePointGPS"]:
			self.subscribe(msg)

	def loop(self):
		time.sleep(self.loop_delay / 1000.0)

		if self.target is None:
			return

		distance = self.position.distance(self.target)
		bearing = self.position.bearing(self.target)

		if distance < self.target_reached_distance:
			self.target = None
			self.publish("DriveStop")
			return

		if abs(bearing) < self.bearing_error and self._rotating:
			self.rotating = False
			self.forward()
		else:
			self.rotating = True
			if bearing < 0:
				self.publish("DriveTurnLeft")
			else:
				self.publish("DriveTurnRight")

	def g_h_filter(z, x0, dx, g, h, dt=1.):
		x_est = x0
		#prediction step
		x_pred = x_est + (dx*dt)
		dx = dx
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
		self.log("heading: "+str(msg.heading))
		self.heading_last = self.heading
		self.heading = compass.heading

	def on_targetGPS(self, pos):
		'''Targets a new GPS coordinate'''
		target = GPSPosition(radians(pos[0]), radians(pos[1]))

		if target.distance(self.position) <= self.maximum_target_distance:
			self.target = target

	def on_singlePointGPS(self, pos):
		'''Updates GPS position'''
		pos_pred_lat = g_h_filter(pos.lat, self.position.lat, 0, 0.1, 0.001)
		pos_pred_lon = g_h_filter(pos.lat, self.position.lon, 0, 0.1, 0.001)
		self.log("{},{}".format(degrees(pos_pred_lat), degrees(pos_pred_lon)))
		self.position_last = self.position
		self.position = GPSPosition(pos_pred_lat, pos_pred_lon)
