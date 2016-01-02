from abc import abstractmethod
from models.aggregates import AggregateModel


class DriveModel(AggregateModel):
    """ Aggregate model to emulate the driving of the rover.
    
    Attributes:
        MAX_SPEED(float) -- The max speed the rover can drive (ie the speed
                            of the rover when power is full.
    Methods:
        update(timeStep) -- Update the position of the rover after `timeStep`
                            has elapsed.
    """
    
    def __init__(self, roverModel):
        AggregateModel.__init__(self, roverModel)
        self.MAX_SPEED = 1 # [m/s]
    
    @abstractmethod
    def update(self, timeStep):
        """ Update the position of the rover after `timeStep` has elapsed.
        
        Pre:
            `roverProperties.position`    The current position of the
                                           rover.
            `roverProperties.powerLeft`   The power to the left side.
            `roverProperties.powerRight`   The power to the right side.
        Post:
            The position of the rover has been updated.
        Return:
            n/a
        """
        print("TODO: implement DriveModel")