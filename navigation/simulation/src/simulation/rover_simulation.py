from models import RoverModel

class RoverSimulation:
        
    # CONSTANTS
    TIME_STEP = 1
    TIME_LIMIT = 1000
    
    def __init__(self):
        self.time = 0
        self.status = False
        
        initialCoordinate = 0
        initialHeading = 0
        destination = 1
        
        self._rover = RoverModel(initialCoordinate, initialHeading, destination)
        
    def runSimulation(self):
        self.time = 0
        notDone = True
        while notDone:
            self.rover.stepTime(self.TIME_STEP)
            notDone = self.rover.checkStatus()
        
        # get status
        self.status = self.rover.wasSuccessful()
        
        return self.status
    
    @property
    def status(self):
        return self._status
    @status.setter 
    def status(self, value):
        self._status = value
    @property
    def rover(self):
        return self._rover
        
    def analyzeResults(self):
        print("TODO: implement analyzeResults method")
    