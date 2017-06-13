from math import asin, atan2, cos, pi, radians, sin, sqrt
from time import sleep

from pyvesc import SetRPM

from .RoverProcess import RoverProcess

class GPSPosition:
    # Earth's radius in metres
    RADIUS = 6371008.8

    def __init__(self, lat, lon):
        # lat an lon are assumed to be in radians
        self.lat = lat
        self.lon = lon

    def distance(self, them):
        ''' Returns the distance to another GPSPositions on earth'''
        hav = lambda z: (1 - cos(z)) / 2   # haversine
        ahav = lambda z: 2 * asin(sqrt(z)) # inverse haversine

        d_lat = them.lat - self.lat
        d_lon = them.lon - self.lon

        z = (hav(d_lat)
             + cos(self.lat) * cos(them.lat) * hav(d_lon))

        return GPSPosition.RADIUS * ahav(z)

    def bearing(self, them):
        ''' Returns the bearing to another GPSPositions on earth'''
        d_lat = them.lat - self.lat
        d_lon = them.lon - self.lon

        y = sin(d_lon) * cos(them.lat)
        x = (cos(self.lat) * sin(them.lat)
             - sin(self.lat) * cos(them.lat) * cos(d_lat))

        return atan2(y, x)

class GPSDriveProcess(RoverProcess):
    '''
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

        for m in ['targetGPS', 'singlePointGPS', 'CompassDataMessage']:
            self.subscribe(m)

    def loop(self):
        sleep(self.loop_delay / 1000.0)

        if self.target is None:
            return

        distance = self.position.distance(self.target)
        bearing = self.position.bearing(self.target)

        if distance < self.target_reached_distance:
            self.target = None
            self._stop()
            return

        if abs(bearing) < self.bearing_error and self._rotating:
            self.rotating = False
            self.forward()
        else:
            self.rotating = True
            if bearing < 0:
                self._turnLeft()
            else:
                self._turnRight()

    def _setLeftWheelSpeed(rpm):
        rpm = SetRPM(int(rpm))
        self.publish("wheelLF", rpm)
        self.publish("wheelLM", rpm)
        self.publish("wheelLB", rpm)

    def _setRightWheelSpeed(rpm):
        rpm = SetRPM(int(rpm))
        self.publish("wheelRF", rpm)
        self.publish("wheelRM", rpm)
        self.publish("wheelRB", rpm)

    def _stop():
        self._setLeftWheelSpeed(0)
        self._setRightWheelSpeed(0)

    def _forward():
        self._setLeftWheelSpeed(MOTOR_RPM)
        self._setRightWheelSpeed(MOTOR_RPM)

    def _backward():
        self._setLeftWheelSpeed(-MOTOR_RPM)
        self._setRightWheelSpeed(-MOTOR_RPM)

    def _turnRight():
        self._setLeftWheelSpeed(MOTOR_RPM)
        self._setRightWheelSpeed(-MOTOR_RPM)

    def _turnLeft():
        self._setLeftWheelSpeed(-MOTOR_RPM)
        self._setRightWheelSpeed(MOTOR_RPM)

    def on_targetGPS(self, pos):
        '''Targets a new GPS coordinate'''
        target = GPSPosition(radians(pos[0]), radians(pos[1]))

        if target.distance(self.position) <= self.maximum_target_distance:
            self.target = target

    def on_CompassDataMessage(self, compass):
        '''Updates current heading'''
        self.heading_last = self.heading
        self.heading = compass.heading

    def on_singlePointGPS(self, pos):
        '''Updates GPS position'''
        self.position_last = self.position
        self.position = GPSPosition(radians(pos[0]), radians(pos[1]))

