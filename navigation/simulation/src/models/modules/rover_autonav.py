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
        
        # update gps coordinate
        self.updateGPSLog()
        
        self.count = self.count + 1
        
        # process GPS data
        if (self.count == 500):
            self.processGPSData()
        
        # make adjustements to roverProperties
        if(self.count == 500):
            bearing = Coordinate.getBearing(self.roverProperties.gpsReading.coordinate, self.roverProperties.DESTINATION)
            
            if(bearing < self.heading):
                self.roverProperties.powerLeft = 0.99
                self.roverProperties.powerRight = 1.0
            else:
                self.roverProperties.powerLeft = 1.0
                self.roverProperties.powerRight = 0.99
                
            count = 0
            
            #self.setPower()
    
    
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
        
        # unpackage to cartesian coordinates relative to first point
        initial_coordinate = self.GPSLog.popleft().coordinate
        x = [0]
        y = [0]
        while self.GPSLog:
            temp = self.GPSLog.popleft()
            distance = Coordinate.getDistance(initial_coordinate, temp.coordinate)
            bearing = Coordinate.getBearing(initial_coordinate, temp.coordinate)
            x.append(distance * sin(radians(bearing)))
            y.append(distance * cos(radians(bearing)))
        
        norm_x = x - np.mean(x)
        norm_y = y - np.mean(y)
        
        cov = np.cov(norm_x, norm_y)
        
        w,v = eig(cov)
        
        if(abs(w[0]) > abs(w[1])):
            v = v[:,0]
        else:
            v = v[:,1]
            
        self.heading = atan2(v[0], v[1]) % 180
        matplot.clf()
        matplot.scatter(x,y, label='Rover Path')
        matplot.plot([0,v[0]], [0,v[1]])
        matplot.show()
        
        #print "heading = " + (atan2(v[1], v[0])*180/3.14159 % 180).__str__()
        
        #self.count
        
    def setPower(self):
        """ Make adjustments to the current properties of the rover to 
        get back on track.
        
        Post:
            `self.roverProperties.powerLeft is updated
            `self.roverProperties.powerRight is updated
        """   
        
        
        
        
        
        