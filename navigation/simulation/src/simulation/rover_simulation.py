from models import RoverModel
from entities import Coordinate

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
        
        initialCoordinate = Coordinate(0,0)
        initialHeading = 0
        destination = Coordinate(0.001, 0.001)
        
        self.TIME_STEP = 0.01
        self.TIME_LIMIT = 1000
        
        self._rover = RoverModel(initialCoordinate, initialHeading, destination)
        
    def runSimulation(self):
        """ Run the simulation.
        
        Return:
            True if the simulation was successful
        """
        self.time = 0
        notDone = True
        while notDone:
            self.rover.stepTime(self.TIME_STEP)
            notDone = self.rover.isComplete()
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
        """ Analyze the results of the simulation. """
        print("TODO: implement analyzeResults method")
    