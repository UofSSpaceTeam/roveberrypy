from models.aggregates import HiddenProperties
from models.aggregates import VisibleProperties
from models.aggregates import DriveModel
from models.aggregates import GPSModel
from models.modules import RoverAutonomousNavigation
from entities.coordinate import Coordinate
from setup import Configuration

class RoverModel(object):
    """ The model of the rover
    
    A model of the rover which will be used for developing an autonomous 
    navigation algorithm.
    
    Methods:
        isComplete() -- Returns true if the rover is at the destination.
        wasSuccessful() -- Return true if the rover reached the destination.
        stepTime(timeStep) -- Update `self` for `timeStep` elapsed time.
    """
    
    
    def __init__(self, initalCoordinate, initialHeading, destination):
        """ Construct an instance of RoverModel
        
        Args:
            initialCoordinate(Coordinate) -- The starting point of the rover.
            initialHeading(Heading) -- The initial direction of the rover.
            destination(Coordinate) -- The destination of the rover.
        """
        self._hiddenProperties = HiddenProperties(initalCoordinate, initialHeading)
        self._visibleProperties = VisibleProperties(destination)
        
        self._models = [DriveModel(self), GPSModel(self), RoverAutonomousNavigation(self)]
    
    
    @property
    def hiddenProperties(self):
        """ The hidden properties of `self`. 
        
        These properties are properties which are used by the simulator to 
        emulate the behavior of the rover. These should not be used
        by modules as there entities which in real life we cannot know the
        exact value of.
        
        For example:
            `position` is the location of the rover in the simulation. In real 
            life we do not know the exact location of the rover -- we only
            know the GPS coordinate which is given by `gpsReading`. Thus 
            `position` is a hidden property and `gpsCoordinate` is the visible
            property. 
        """
        return self._hiddenProperties
    
    
    @property
    def visibleProperties(self):
        """ The visible properties of `self`.
        
        These are the properties which are to be used by modules. For a more 
        in-depth description of access priviledges see 
        `RoverModel.hiddenProperties`
        """
        return self._visibleProperties
    
    
    def isComplete(self):
        """ Returns true if the rover is at the destination """
        COMPLETION_TOLERANCE = Configuration.get('simulation.destination.tolerance')
        distance = Coordinate.getDistance(self.visibleProperties.DESTINATION, self.hiddenProperties.position)
        if( distance < COMPLETION_TOLERANCE):
            return True
        else:
            return False
    
    def stepTime(self, timeStep):
        """ Update the rover model after `timeStep` has elapsed.
        
        All aggregate models are updated and then all modules are updated.
        """
        for model in self._models:
            model.update(timeStep)
                
    def wasSuccessful(self):
        """ Returns true if the rover reached the destination """
        return False