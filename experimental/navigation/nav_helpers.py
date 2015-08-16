from math import pi, asin, sqrt, sin, cos, atan2

#haversin formula
def haversin(theta):
    return sin(theta/2)*sin(theta/2)

#******************************************************************************#
#                       C O O R D I N A T E   C L A S S                        #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  #
#   Attributes:                                                                #
#       lat         ::  latitude                                               #
#       lon         ::  longitude                                              #
#       RE          ::  radius of the earth in Poland                          #
#   Member Funcions:                                                           #
#       distanceTo(CoordinateObject)    ::  distance [m] to CoordinateObject   #
#                                           from #self                         #
#       bearingTo(CoordinateObject)     ::  absolute bearing to                #
#                                           CoordinateObject from #self        #
#******************************************************************************#

class Coordinate:
    lat = -1        # latitude in DD
    lon = -1        # longitude in DD
    RE = 6364843    # radius of the earth in poland
    # constuct with longitude and latitude if it exists
    def __init__(self, latitude = -1, longitude = -1, heading = -1):
        self.lat = latitude
        self.lon = longitude
    # get the distance to another coordinate
    def distanceTo(self, coord):
        lat1 = self.lat * pi / 180
        lon1 = self.lon * pi / 180
        lat2 = coord.lat * pi/ 180
        lon2 = coord.lon * pi / 180
        return (2*self.RE*asin( sqrt( haversin(lat2-lat1) +
                                 cos(lat1)*cos(lat2)*haversin(lon2-lon1))))
    # get the bearing to another coordinate
    def bearingTo(self, coord):
        lat1 = self.lat * pi / 180
        lon1 = self.lon * pi / 180
        lat2 = coord.lat * pi/ 180
        lon2 = coord.lon * pi / 180
        bearing = (atan2(sin(lon2-lon1)*cos(lat2),
                         cos(lat1)*sin(lat2)
                         -sin(lat1)*cos(lat2)*cos(lon2-lon1)))
        while(bearing < 0):
            bearing = bearing + 2*pi
        while(bearing > 2*pi):
            bearing = bearing - 2*pi
        return bearing * 180/pi

#******************************************************************************#
#               E N D   O F   C O O R D I N A T E   C L A S S                  #
#******************************************************************************#



#-------------------------------------------------------------------------------



#******************************************************************************#
#               C O O R D I N A T E S   T E S T   C A S E                      #
#******************************************************************************#


# test case from (43.990967, 78.48321) to (43.991, 78.4833)
# the result should be that y is 8 meters to at a bearing of 63[deg]

#x = Coordinate(43.990967, 78.48321)
#y = Coordinate(43.991, 78.4833)
#print("Distance from x to y is: ", x.distanceTo(y))
#print("Bearing from x to y is: ", x.bearingTo(y))
