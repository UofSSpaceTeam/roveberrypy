from models import BaseModelClass
from _collections import deque
import numpy as np
from numpy.linalg import eig
from sklearn.decomposition import PCA
from entities.coordinate import Coordinate
from math import radians, sin, cos, atan2
import matplotlib.pyplot as matplot
from entities.gps_coordinate import GPSCoordinate

class RoverAutonomousNavigation(BaseModelClass):
    """ Autonomous navigation algorithm
    
    The algorithm which will be used to drive the rover autonomously from one
    location (coordinate) to the next.
    """
    
    GPSLog = None
    
    count = None
    heading = None
    
    def __init__(self, roverModel):
        BaseModelClass.__init__(self, roverModel)
        self.GPSLog = deque([],100)
        self.count = 0
        heading = 0
        
    def update(self, timeStep):
        """ Update the drive commands to the rover.
        
        Pre:
            `roverProperties.gpsReading` has been updated with the current GPS
                                         coordinate
        Post:
            `roverProperties.powerLeft` has been updated
            `roverProperties.powerRight` has been updated
        """        
    
    
    def updateGPSLog(self):
        """ Update the GPS log. This function is here to couple the rover to 
        this class.
        
        Post:
            `self.GPSLog is updated
        """    
        
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
        
        
        
        
        
        