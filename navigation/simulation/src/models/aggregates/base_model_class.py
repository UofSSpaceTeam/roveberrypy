from abc import ABCMeta
from abc import abstractmethod
from models.aggregates import RoverProperties


class BaseModelClass(object):
    """ Abstract base class for a RoverModel aggregate model. 
    
    Abstract methods:
        update(timeStep) -- update the model after `timeStep` has elapsed.
    """
    
    __metaclass__ = ABCMeta
    
    
    def __init__(self, roverModel):
        """ Constructor for base class.
        
        Args:
            roverModel(RoverModel) -- Rover model instance
        """
        self._roverProperties = RoverProperties(roverModel)
        
        
    @property
    def roverProperties(self):
        """ The properties of the rover model instance.
        
        Note:
            There is no setter for this property.
        """
        return self._roverProperties
    
    
    @abstractmethod
    def update(self, timeStep):
        """ Update the rover models properties after `timeStep` has elapsed.
        
        Note:
            This is method must be overriden.
        """
        return


class AggregateModel(BaseModelClass):
    """ Abstract base class for a RoverModel aggregate model
        
    Note:
        This class is simply a BaseModelClass with permission to access hidden 
        properties of `roverProperties`
    """
    
    def __init__(self, roverModel):
        """ See `BaseModelClass.__init__` """
        BaseModelClass.__init__(self, roverModel)
        self._roverProperties.grantHiddenAccess()
# eof