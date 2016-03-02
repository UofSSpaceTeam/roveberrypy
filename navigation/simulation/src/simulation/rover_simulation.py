from models import RoverModel
from entities import Coordinate
from math import radians, sin, cos
from setup import Configuration
from setup import DemoConfiguration

class RoverSimulation:
    """ Run a simulation of the rover.
    
    This class is used to run a simulation of the USST's rover.
    
    Attributes:
        TIME_STEP -- The size of the time step to use in the simulation. This
                     is how many seconds passes between updates to the rover
                     model
        TIME_LIMIT -- The maximum allowed time given to the rover to get to
                      the destination.
    Methods:
        runSimulation() -- Run the simulation.
        analyzeResults() -- Analyze the results of the simulation.
    """ 
    
    def __init__(self):
        self.time = 0
        self.status = False
        
        initialLatitude = Configuration.get('rover_model.initial_conditions.latitude')
        initialLongitude = Configuration.get('rover_model.initial_conditions.longitude')
        initialCoordinate = Coordinate(initialLatitude, initialLongitude)
        initialHeading = DemoConfiguration.get('t0.heading') #Configuration.get('rover_model.initial_conditions.heading')
        destLatitude = Configuration.get('simulation.destination.latitude')
        destLongitude = Configuration.get('simulation.destination.longitude')
        destination = Coordinate(destLatitude, destLongitude)
        
        self.TIME_STEP = Configuration.get('simulation.time_step')
        self.TIME_LIMIT = Configuration.get('simulation.time_limit')
        
        self._rover = RoverModel(initialCoordinate, initialHeading, destination)
        
    def runSimulation(self):
        """ Run the simulation.
        
        Return:
            True if the simulation was successful
        """
        self.time = 0
        notDone = True
        while notDone and self.time < self.TIME_LIMIT:
            if(self.time > 0):
                self.rover.visibleProperties.powerLeft = DemoConfiguration.get('t0.left')
                self.rover.visibleProperties.powerRight = DemoConfiguration.get('t0.right')
            if(self.time > 1):
                self.rover.visibleProperties.powerLeft = DemoConfiguration.get('t1.left')
                self.rover.visibleProperties.powerRight = DemoConfiguration.get('t1.right')
            if(self.time > 2):
                self.rover.visibleProperties.powerLeft = DemoConfiguration.get('t2.left')
                self.rover.visibleProperties.powerRight = DemoConfiguration.get('t2.right')
            if(self.time > 3):
                self.rover.visibleProperties.powerLeft = DemoConfiguration.get('t3.left')
                self.rover.visibleProperties.powerRight = DemoConfiguration.get('t3.right')
            if(self.time > 4):
                self.rover.visibleProperties.powerLeft = DemoConfiguration.get('t4.left')
                self.rover.visibleProperties.powerRight = DemoConfiguration.get('t4.right')
            if(self.time > 5):
                self.rover.visibleProperties.powerLeft = DemoConfiguration.get('t5.left')
                self.rover.visibleProperties.powerRight = DemoConfiguration.get('t5.right')
            if(self.time > 6):
                self.rover.visibleProperties.powerLeft = DemoConfiguration.get('t6.left')
                self.rover.visibleProperties.powerRight = DemoConfiguration.get('t6.right')
            if(self.time > 7):
                self.rover.visibleProperties.powerLeft = DemoConfiguration.get('t7.left')
                self.rover.visibleProperties.powerRight = DemoConfiguration.get('t7.right')
            if(self.time > 8):
                self.rover.visibleProperties.powerLeft = DemoConfiguration.get('t8.left')
                self.rover.visibleProperties.powerRight = DemoConfiguration.get('t8.right')
            if(self.time > 9):
                self.rover.visibleProperties.powerLeft = DemoConfiguration.get('t9.left')
                self.rover.visibleProperties.powerRight = DemoConfiguration.get('t9.right')
            self.rover.stepTime(self.TIME_STEP)
            notDone = not(self.rover.isComplete())
            self.time += self.TIME_STEP
        # get status
        self.status = self.rover.wasSuccessful()
        return self.status
    
    @property
    def status(self):
        """ The status of the simulation. """
        return self._status
    
    @status.setter 
    def status(self, value):
        self._status = value
        
    @property
    def rover(self):
        """ The instance of the RoverModel object. """
        return self._rover
        
    def analyzeResults(self):
        """ Analyze the results of the simulation.
            
            Convert the distances and bearings of the rover to x-y coordinates,
            and output the values to a "filename.txt"
        """
        
        tempLog = self.rover.hiddenProperties.positionLog
        tempGPSLog = self.rover.visibleProperties.allGPSReadings
        initialCoordinate = tempLog[0]
        distances = [None]* len(self.rover.hiddenProperties.positionLog)
        bearings = [None] * len(self.rover.hiddenProperties.positionLog)
        x = [None] * len(self.rover.hiddenProperties.positionLog)
        y = [None] * len(self.rover.hiddenProperties.positionLog)
        gps_distances = [None]* len(self.rover.visibleProperties.allGPSReadings)
        gps_bearings = [None] * len(self.rover.visibleProperties.allGPSReadings)
        gps_x = [None] * len(self.rover.visibleProperties.allGPSReadings)
        gps_y = [None] * len(self.rover.visibleProperties.allGPSReadings)
        
        dest_dist = Coordinate.getDistance(initialCoordinate, self.rover.visibleProperties.DESTINATION)
        dest_heading = Coordinate.getBearing(initialCoordinate, self.rover.visibleProperties.DESTINATION)
        dest_x = dest_dist * sin(radians(dest_heading))
        dest_y = dest_dist * cos(radians(dest_heading))

        "create list of distances and bearings"
        for i in range(0, len(self.rover.hiddenProperties.positionLog)-1):
            distances[i]= Coordinate.getDistance(initialCoordinate, tempLog[i])
            bearings[i] = Coordinate.getBearing(initialCoordinate, tempLog[i])
            gps_distances[i] = Coordinate.getDistance(initialCoordinate, tempGPSLog[i].coordinate)
            gps_bearings[i] = Coordinate.getBearing(initialCoordinate, tempGPSLog[i].coordinate)
                
        "convert distances and bearings to x-y coordinates"
        for i in range(0, len(self.rover.hiddenProperties.positionLog)-1):
            x[i] = (distances[i]) * sin(radians(bearings[i]))
            y[i] = (distances[i]) * cos(radians(bearings[i]))
            gps_x[i] = (gps_distances[i]) * sin(radians(gps_bearings[i]))
            gps_y[i] = (gps_distances[i]) * cos(radians(gps_bearings[i]))
            
        "Write data to file"
        import matplotlib.pyplot as matplot
        matplot.plot(x,y, label='Rover Path')
        matplot.scatter(gps_x, gps_y,marker='^',color='g',s=3, label='GPS Readings')
        #matplot.scatter([dest_x], [dest_y], marker='o', color='r', s=5, label='Destination')
        #matplot.scatter([0], [0], marker='o', color='g', s=5, label='Start')
        matplot.title("Autonomous Navigation Simulation Results")
        matplot.xlabel("Relative Position, [m]")
        matplot.ylabel("Relative Position, [m]")
        matplot.legend(shadow=True)
        matplot.gca().set_aspect('equal', adjustable='box')
        matplot.show()
            