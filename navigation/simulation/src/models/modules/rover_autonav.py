from models import BaseModelClass

class RoverAutonomousNavigation(object):
    
    def __init__(self, roverModel):
        BaseModelClass.__init__(self, roverModel)
        
    def update(self, timeStep):
        print("TODO: implement RoverNavigation")