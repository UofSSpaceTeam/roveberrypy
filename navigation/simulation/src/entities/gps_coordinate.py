class GPSCoordinate(object):
    """ Used to represent a GPS reading.
    
    Properties:
        coordinate(Coordinate) -- The GPS coordinate.
        time(TimeStamp) -- The time of the GPS reading.
    Methods:
        __str__() -- convert to string
    """
    def __init__(self, coordinate, timeStamp):
        self._coordinate = coordinate
        self._time = timeStamp
        
    @property
    def coordinate(self):
        """ The GPS coordinate.
        
        Note:
            Not modifiable
        """
        return self._coordinate
    
    @property
    def time(self):
        """ The time of the GPS reading.
        
        Note:
            Not modifiable
        """
        return self._time
    
    def __str__(self):
        """ Convert to string. """
        return self.coordinate.__str__() + "\n" + self.time.__str__()
    
    
        