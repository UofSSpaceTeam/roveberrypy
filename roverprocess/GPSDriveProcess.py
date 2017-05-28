from math import asin, atan2, cos, radians, sin, sqrt

from .RoverProcess import RoverProcess

# haversine function
hav = lambda z: (1 - cos(z)) / 2

# inverse haversine function
ahav = lambda z: 2 * asin(sqrt(z))

EARTH_RADIUS = 6371008.8

class GPSPosition:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def distance(self, them):
        ''' Returns the distance to another GPSPositions on earth'''
        s_lat, s_lon = self.radians()
        t_lat, t_lon = them.radians()

        d_lat = t_lat - s_lat
        d_lon = t_lon - s_lon

        z = hav(d_lat) + cos(s_lat)*cos(t_lat)*hav(d_lon)

        return EARTH_RADIUS * ahav(z)

    def bearing(self, them):
        ''' Returns the bearing to another GPSPositions on earth'''
        s_lat, s_lon = self.radians()
        t_lat, t_lon = them.radians()

        d_lat = t_lat - s_lat
        d_lon = t_lon - s_lon

        y = sin(d_lon)*cos(t_lat)
        x = cos(s_lat)*sin(t_lat) - sin(s_lat)*cos(t_lat)*cos(d_lat)

        return atan2(y, x)

    def radians(self):
        '''Returns a tuple of latitude and longitude in radians'''
        return (radians(self.lat), radians(self.lon))

class GPSDriveProcess(RoverProcess):
    '''
    '''
    def setup(self, args):
        self.subscribe('singlePointGPS')
        self.current_position = None
        self.target_position = None
        self.last_position = None

    def on_singlePointGPS(self, pos):
        self.last_position = self.current_position
        self.current_position = GPSPosition(pos[0], pos[1])

        if self.last_position is not None:
            distance = self.last_position.distance(self.current_position)
            bearing  = self.last_position.bearing(self.current_position)
            self.log("distance: {}, bearing: {}".format(distance, bearing))


