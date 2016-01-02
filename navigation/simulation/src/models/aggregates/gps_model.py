from models.aggregates import BaseModelClass

class GPSModel(object):

    def __init__(self, roverModel):
        BaseModelClass.__init__(self, roverModel)
        self.roverProperties.grantHiddenAccess()
        
        self.NUM_READINGS = 10
        
    @property
    def roverProperties(self):
        return self._roverProperties
    
    @property
    def time(self):
        return self._time
    @time.setter 
    def time(self, value):
        self._time = value
    
    def update(self, timeStep):
        print("TODO: implement GPS model")
        
        