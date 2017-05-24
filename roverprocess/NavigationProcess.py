from .RoverProcess import RoverProcess

class NavigationProcess(RoverProcess):

    def setup(self, args):
        self.subscribe("LidarDataMessage")

    def on_LidarDataMessage(self, lidarmsg):
        self.log("Dist: "+str(lidarmsg.distance)+
                 " Angle: "+str(lidarmsg.angle))
