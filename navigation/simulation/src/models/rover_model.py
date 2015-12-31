from models import HiddenProperties
from models import VisibleProperties

class RoverModel(object):

    # constructor for rover model instance
    def __init__(self, initalCoordinate, initialHeading, destination):
        self._hiddenProperties = HiddenProperties(initalCoordinate, initialHeading)
        self._visibleProperties = VisibleProperties(destination)
        self._models = [] # TODO: add models here
    
    # hidden properties. Copied instance is linked to this object
    @property
    def hiddenProperties(self):
        return self._hiddenProperties
    
    # visible properties. Copied instance is linked to this object
    @property
    def visibleProperties(self):
        return self._visibleProperties
    
    # completion check
    def isComplete(self):
        #TODO: implement completion check
        return False
    
    # method for updating the models after a time step
    def stepTime(self, timeStep):
        for model in self._models:
            model.update(timeStep)
    
            