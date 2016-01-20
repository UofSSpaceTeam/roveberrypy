from models import RoverModel
from entities import Coordinate
from math import radians, sin, cos
from setup import Configuration

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
        initialHeading = Configuration.get('rover_model.initial_conditions.heading')
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
        initialCoordinate = tempLog[0]
        distances = [None]* len(self.rover.hiddenProperties.positionLog)
        bearings = [None] * len(self.rover.hiddenProperties.positionLog)
        x = [None] * len(self.rover.hiddenProperties.positionLog)
        y = [None] * len(self.rover.hiddenProperties.positionLog)
        

        "create list of distances and bearings"
        for i in range(0, len(self.rover.hiddenProperties.positionLog)-1):
            distances[i]= Coordinate.getDistance(initialCoordinate, tempLog[i])
            bearings[i] = Coordinate.getBearing(initialCoordinate, tempLog[i])
         
        "convert distances and bearings to x-y coordinates"
        for i in range(0, len(self.rover.hiddenProperties.positionLog)-1):
            x[i] = (distances[i]) * sin(radians(bearings[i]))
            y[i] = (distances[i]) * cos(radians(bearings[i]))
            
        "Write data to file"
        file = open("../../scratch/output.csv", "w") 
        for coord in range(0,len(x)-1):
            file.write(str(x[coord]) + ',' + str(y[coord]))
            file.write('\n')
            