from models import BaseModelClass

class RoverAutonomousNavigation(BaseModelClass):
    """ Autonomous navigation algorithm
    
    The algorithm which will be used to drive the rover autonomously from one
    location (coordinate) to the next.
    """
    def __init__(self, roverModel):
        BaseModelClass.__init__(self, roverModel)
        
    def update(self, timeStep):
        """ Update the drive commands to the rover.
        
        Pre:
            `roverProperties.gpsReading` has been updated with the current GPS
                                         coordinate
        Post:
            `roverProperties.powerLeft` has been updated
            `roverProperties.powerRight` has been updated
        """
        print("TODO: implement RoverNavigation")