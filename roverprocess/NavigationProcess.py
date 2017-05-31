from .RoverProcess import RoverProcess

class NavigationProcess(RoverProcess):

    def setup(self, args):
        for msg in ["LidarDataMessage", "CompassDataMessage"]:
            self.subscribe(msg)

    def on_LidarDataMessage(self, lidarmsg):
        self.log("Dist: "+str(lidarmsg.distance)+
                 " Angle: "+str(lidarmsg.angle))

    def on_CompassDataMessage(self, msg):
        self.log("heading: "+str(msg.heading))

