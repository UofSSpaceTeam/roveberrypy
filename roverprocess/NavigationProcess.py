from .RoverProcess import RoverProcess

class NavigationProcess(RoverProcess):
    ''' Aggregates data from GPS, Magnetometer, LIDAR, etc,
        and makes driving decisions based on the rover's
        surroundings.
    '''

    def setup(self, args):
        for msg in ["LidarDataMessage", "CompassDataMessage"]:
            self.subscribe(msg)

    def on_LidarDataMessage(self, lidarmsg):
        ''' LidarDataMessage contains:
            distance (centimeters): The lidar unit fires a laser
                beam directly forwards. When it hits an object,
                the length of this beam is the distance.
            angle (degrees): The angle at which the distance
                measurement was taken.
        '''
        self.log("Dist: "+str(lidarmsg.distance)+
                 " Angle: "+str(lidarmsg.angle))

    def on_CompassDataMessage(self, msg):
        ''' CompassDataMessage contains:
            heading (degrees): Relative to north, the angle of
                rotation on the axis normal to the earth's surface.
            pitch (degrees):
            roll (degrees):
        '''
        self.log("heading: "+str(msg.heading))

