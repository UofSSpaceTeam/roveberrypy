import abc
from models.aggregates import BaseModelClass

class DriveModel(BaseModelClass):
    
    def __init__(self, roverModel):
        BaseModelClass.__init__(self, roverModel)
        self.roverProperties.grantHiddenAccess()
        
        self.MAX_SPEED = 1 # [m/s]
    
    @abc.abstractmethod
    def update(self, timeStep):
        print("TODO: implement DriveModel")