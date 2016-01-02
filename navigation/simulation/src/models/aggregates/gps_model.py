from models.aggregates import AggregateModel

class GPSModel(AggregateModel):
    """ Aggregate model to emulate the rover's GPS system.
    
    Attributes:
        RADIAL_ACCURACY(float) -- The radial accuracy of the GPS system [m] 
    Methods:
        update(timeStep) -- Update the GPS reading
    """
    
    
    def __init__(self, roverModel):
        """ See `BaseModelClass.__init__(roverModel)` """
        AggregateModel.__init__(self, roverModel)
        
    
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
        print("TODO: implement GPS model")
        
        