from models.aggregates import AggregateModel
from entities import TimeStamp
from entities import GPSCoordinate
from random import gauss
from entities.coordinate import Coordinate
from setup import Configuration

class GPSModel(AggregateModel):
    """ Aggregate model to emulate the rover's GPS system.
    
    Attributes:
        STD_LAT(float) -- The standard deviation in latitude measurements.
        STD_LON(float) -- The standard deviation in longitude measurements.
    Methods:
        update(timeStep) -- Update the GPS reading
    """
    
    STD_LAT = None
    STD_LON = None
    
    def __init__(self, roverModel):
        """ See `BaseModelClass.__init__(roverModel)` """
        AggregateModel.__init__(self, roverModel)
        self._time = TimeStamp(0, 0, 0)
        
        self.STD_LAT = Configuration.get('rover_model.aggregates.gps_model.std_lat')
        self.STD_LON = Configuration.get('rover_model.aggregates.gps_model.std_lon')
    
    @property
    def time(self):
        """ The time in the simulation.
        
        Note:
            This property is updated whenever the `update` method is called.
        """
        return self._time
    
    @time.setter 
    def time(self, value):
        self._time = value
    
    
    def update(self, timeStep):
        """ Update the rover's GPS coordinate.
        
        Pre:
            `roverProperties.position`  is the current absolute position in the
                                        simulation.
        Post:
            `roverProperties.gpsReading`    is updated.
        Return:
            n/a
        """
        self.time = self.time + timeStep
        
        # create random GPS coordinate near the actual position
        position = self.roverProperties.position.dd
        latitude = position.latitude
        longitude = position.longitude
        latReading = gauss(latitude, self.STD_LAT)
        lonReading = gauss(longitude, self.STD_LON)
        self.roverProperties.gpsReading = GPSCoordinate(Coordinate(latReading, lonReading), self.time)
        
        
        