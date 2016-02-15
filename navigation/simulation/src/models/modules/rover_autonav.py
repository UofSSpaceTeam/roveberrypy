from models import BaseModelClass
from _collections import deque

class RoverAutonomousNavigation(BaseModelClass):
    """ Autonomous navigation algorithm
    
    The algorithm which will be used to drive the rover autonomously from one
    location (coordinate) to the next.
    """
    
    GPSLog = None
    
    def __init__(self, roverModel):
        BaseModelClass.__init__(self, roverModel)
        self.GPSLog = deque([],10)
        
    def update(self, timeStep):
        """ Update the drive commands to the rover.
        
        Pre:
            `roverProperties.gpsReading` has been updated with the current GPS
                                         coordinate
        Post:
            `roverProperties.powerLeft` has been updated
            `roverProperties.powerRight` has been updated
        """        
        
        # update gps coordinate
        self.updateGPSLog()
        
        # process GPS data
        self.processGPSData()
        
        # make adjustements to roverProperties
        self.setPower()
    
    
    def updateGPSLog(self):
        """ Update the GPS log. This function is here to couple the rover to 
        this class.
        
        Post:
            `self.GPSLog is updated
        """    
        self.GPSLog.append(self.roverProperties.gpsReading)
        
    def processGPSData(self):
        """ Process the current GPS data.
        
        Post:
            `self.position is updated
            `self.heading is updated
        """
        
        
    def setPower(self):
        """ Make adjustments to the current properties of the rover to 
        get back on track.
        
        Post:
            `self.roverProperties.powerLeft is updated
            `self.roverProperties.powerRight is updated
        """   
        
        
        
        
        
        