from math import pi, asin, sqrt, sin, cos, atan2, radians, degrees, floor

class Coordinate(object):
    """ Used to represent a coordinate in DD, DMS, or DDM format
    Static Methods:
    getDistance(startCoordinate, startCoordinate) -- Get the distance 
    between two 
    coordinates.
    getBearing(startCoordinate, endCoordinate) -- Get the bearing between
     two coordinates
    shiftCoordinate(startCoordinate, bearing, distance) -- Get a shifted
                                                          coordinate
    """
    def __init__(self, latitude, longitude):
        """ Construct an instance of `Coordinate`
        Args:
        latitude(float) -- The latitude of the coordinate in degrees.
        longitude(float) -- The longitude of the coordinate in degrees.
        """
        # Decimal Degrees
        lat_dd = latitude
        lon_dd= longitude
        self._dd = FormattedLatLong(lat_dd, lon_dd)
        # Degree Minute Seconds
        lat_dms_d = floor(latitude)
        lat_dms_m = floor((latitude - lat_dms_d) * 60)
        lat_dms_s = (latitude - lat_dms_d - lat_dms_m / 60) * 3600
        lon_dms_d = floor(longitude)
        lon_dms_m = floor((longitude - lon_dms_d) * 60)
        lon_dms_s = (longitude - lon_dms_d - lon_dms_m / 60) * 3600
        self._dms = FormattedLatLong(DMS(lat_dms_d, lat_dms_m, lat_dms_s), DMS(lon_dms_d, lon_dms_m, lon_dms_s))
        # Degree Decimal Minutes
        lat_ddm_d = floor(latitude)
        lat_ddm_dm = (latitude - lat_ddm_d) * 60
        lon_ddm_d = floor(longitude)
        lon_ddm_dm = (longitude - lon_ddm_d) * 60
        self._ddm = FormattedLatLong(DDM(lat_ddm_d, lat_ddm_dm), DDM(lon_ddm_d, lon_ddm_dm))
        
        
    @property
    def dms(self):
        """ The coordinate represented in DMS format.
        Note: there is no setter for this property.
        """
        return self._dms
    
    @property
    def ddm(self):
        """ The coordinate represented in DDM format. 
        Note: there is no setter for this property.
        """
        return self._ddm
    
    @property
    def dd(self):
        """ The coordinate represented in DD format. 
        Note: there is no setter for this property.
        """
        return self._dd
    
    def __str__(self):
        return str(self.dd.latitude) + "N, " + str(self.dd.longitude) + "W"
    
    def toDDCoordinate(self):
        return DDCoordinate(self.latitude.dd, self.longitude.dd)
    
    def toDDMCoordinate(self):
        return DDMCoordinate(self.ddm.latitude, self.ddm.longitude)
    
    def toDMSCoordinate(self):
        return DMSCoordinate(self.dms.latitude, self.dms.longitude)
    
    @staticmethod
    def getDistance(startCoordinate, endCoordinate):
        """ Get the distance between two coordinates
        Args:
        startCoordinate(Coordinate) -- The staring coordinate.
        endCoordinate(Coordinate) -- The ending coordinate.
        Return:
        The distance between the two coordinates in meters.
        """
        # mean radius of the earth
        RE = 6371000
        # define harversin function
        def haversin(theta):
            return sin(theta/2)*sin(theta/2) 
        # get too and from coordinates in radians
        lat1 = radians(startCoordinate.dd.latitude)
        lon1 = radians(startCoordinate.dd.longitude)
        lat2 = radians(endCoordinate.dd.latitude)
        lon2 = radians(endCoordinate.dd.longitude)
        # calculate the distance
        distance = (2*RE*asin( sqrt( haversin(lat2-lat1) + cos(lat1)*cos(lat2)*haversin(lon2-lon1))))
        #return the distance
        return distance
    
    @staticmethod
    def getBearing(startCoordinate, endCoordinate):
        """ Get the bearing between two coordinates.
        Args:
        startCoordinate(Coordinate) -- The staring coordinate.
        endCoordinate(Coordinate) -- The ending coordinate.
        Return:
        The bearing between the two coordinates in degrees.
        """
        # get too and from coordinates
        lat1 = radians(startCoordinate.dd.latitude)
        lon1 = radians(startCoordinate.dd.longitude)
        lat2 = radians(endCoordinate.dd.latitude)
        lon2 = radians(endCoordinate.dd.longitude)
        # calculate the bearing
        bearing = (atan2(sin(lon2-lon1)*cos(lat2), cos(lat1)*sin(lat2) -sin(lat1)*cos(lat2)*cos(lon2-lon1)))
        return degrees(bearing % (2*pi))
    
    @staticmethod
    def shiftCoordinate(startCoordinate, bearing, distance):
        """ Shift a coordinate.
        Args:
        startCoordinate(Coordinate) -- The staring coordinate.
        bearing(float) -- The bearing of the new coordinate relative to
         `startCoordinate`, in degrees.
        distance(float) -- The distance from `startCoordinate` to the new
          coordinate in meters.
        Return:
        The distance between the two coordinates in meters.
        """
        # mean radius of the earth
        RE = 6371000
        #convert bearing to radians
        bearing = radians(bearing)
        # get start location
        lat1 = radians(startCoordinate.dd.latitude)
        lon1 = radians(startCoordinate.dd.longitude)
        delta = distance/RE
        # calculate latitude
        latitude = asin(sin(lat1)*cos(delta) + cos(lat1)*sin(delta)*cos(bearing))
        longitude = lon1 + atan2(sin(bearing)*sin(delta)*cos(lat1), cos(delta)-sin(lat1)*sin(latitude))
        # return new coordinate
        return Coordinate(degrees(latitude), degrees(longitude))

class DMSCoordinate(Coordinate):
    """ Create a coordinate from a DMS coordinate format.
    This class is the exact same as `Coordinate` except its constructor takes
    DMS formatted arguments.
    """
    def __init__(self, latitude, longitude):
        """ Create a `Coordinate` from DMS formatted arguments 
        Args:
        latitude(object) -- Latitude with attributes `.d`, `.m`, and `.s`
        longitude(object) -- Longitude with attributes `.d`, `.m`, and `.s`
        """
        latitude = latitude.d + latitude.m/60 + latitude.s/3600
        longitude = longitude.d + longitude.m/60 + longitude.s/3600
        Coordinate.__init__(self, latitude, longitude)
    
    def __str__(self):
        return str(self.dms.latitude.d) + " " + str(self.dms.latitude.m) + " " + str(self.dms.latitude.s) + "N, " + \
               str(self.dms.longitude.d) + " " + str(self.dms.longitude.m) + " " + str(self.dms.longitude.s) + "W"
    
class DDMCoordinate(Coordinate):
    """ Create a coordinate from a DDM coordinate format.
    This class is the exact same as `Coordinate` except its constructor takes
    DDM formatted arguments.
    """
    def __init__(self, latitude, longitude):
        """ Create a `Coordinate` from DDM formatted arguments 
        Args:
        latitude(object) -- Latitude with attributes `.d`, and `.dm`
        longitude(object) -- Longitude with attributes `.d`, and`.dm`
        """
        latitude = latitude.d + latitude.dm / 60
        longitude = longitude.d + longitude.dm / 60
        Coordinate.__init__(self, latitude, longitude)
        
    def __str__(self):
        return str(self.ddm.latitude.d) + " " + str(self.ddm.latitude.dm) + "N, " + \
               str(self.ddm.longitude.d) + " " + str(self.ddm.longitude.dm) + "W"

class DDCoordinate(Coordinate):
    """ Create a coordinate from a DD coordinate format.
    This class is the exact same as `Coordinate` except its constructor takes
    DD formatted arguments.
    """
    def __init__(self, latitude, longitude):
        """ Create a `Coordinate` from DD formatted arguments 
        Args:
        latitude(object) -- Latitude in degrees.
        longitude(object) -- Longitude in degrees.
        """
        Coordinate.__init__(self, latitude, longitude)
        





"""    Nested Property Work-around helpers    """ 

class DD(object):
    def __init__(self, dd):
        self.dd = dd        
        
class DDM(object):
    def __init__(self, d, dm):
        self.d = d
        self.dm = dm 

class DMS(object):
    def __init__(self, d, m, s):
        self.d = d
        self.m = m 
        self.s = s

class FormattedLatLong(object):
    def __init__(self, lat_dd, lon_dd):
        self.latitude = lat_dd 
        self.longitude = lon_dd 
        
    
    
    
    