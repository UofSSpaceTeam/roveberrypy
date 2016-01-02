import abc
from models.aggregates import RoverProperties

class BaseModelClass(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, roverModel):
        self._roverProperties = RoverProperties(roverModel)
        
    @property
    def roverProperties(self):
        return self._roverProperties
    
    @abc.abstractmethod
    def update(self, timeStep):
        # update the rover properties handled by this model after a time change
        # of timeStep
        return

