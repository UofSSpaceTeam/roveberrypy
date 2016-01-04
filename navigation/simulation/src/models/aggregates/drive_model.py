from abc import abstractmethod
from models.aggregates import AggregateModel
from math import sqrt, cos, pi, sin, asin, isnan, atan2
from entities.coordinate import Coordinate
from random import gauss


class DriveModel(AggregateModel):
    """ Aggregate model to emulate the driving of the rover.
    
    Attributes:
        MAX_SPEED(float) -- The max speed the rover can drive (ie the speed
                            of the rover when power is full.
    Methods:
        update(timeStep) -- Update the position of the rover after `timeStep`
                            has elapsed.
    """
    
    MAX_SPEED = 1 # [m/s]
    ROVER_WIDTH = 0.8 # [m]
    
    def __init__(self, roverModel):
        AggregateModel.__init__(self, roverModel)
        
        # TEMPORARY DEFAULT CONDITION
        self.roverProperties.powerLeft = gauss(1, 1e-4)
        self.roverProperties.powerRight = gauss(0.5, 1e-4)
        
        self.v_x = 0
        self.v_y = 1
        self.omega_z = 1e-6
        
        
    @property
    def v_x(self):
        return self._v_x
    @v_x.setter 
    def v_x(self, value):
        self._v_x = value
        
    @property
    def v_y(self):
        return self._v_y
    @v_y.setter 
    def v_y(self, value):
        self._v_y = value
        
    @property
    def x_ICR_v(self):
        return self._x_ICR_v
    @x_ICR_v.setter 
    def x_ICR_v(self, value):
        self._x_ICR_v = value
        
    @property
    def x_ICR_l(self):
        return self._x_ICR_l
    @x_ICR_l.setter 
    def x_ICR_l(self, value):
        self._x_ICR_l = value
        
    @property
    def x_ICR_r(self):
        return self._x_ICR_r
    @x_ICR_r.setter 
    def x_ICR_r(self, value):
        self._x_ICR_r = value
        
    @property
    def y_ICR_v(self):
        return self._y_ICR_v
    @y_ICR_v.setter 
    def y_ICR_v(self, value):
        self._y_ICR_v = value
        
    @property
    def omega_z(self):
        return self._omega_z
    @omega_z.setter 
    def omega_z(self, value):
        self._omega_z = value
    
    @abstractmethod
    def update(self, timeStep):
        """ Update the position of the rover after `timeStep` has elapsed.
        
        Pre:
            `roverProperties.position`    The current position of the
                                           rover.
            `roverProperties.powerLeft`   The power to the left side.
            `roverProperties.powerRight`   The power to the right side.
        Post:
            The position of the rover has been updated.
        Return:
            n/a
        """
        # Get left and right wheel velocities
        veloLeft = self.roverProperties.powerLeft * self.MAX_SPEED
        veloRight = self.roverProperties.powerRight * self.MAX_SPEED
        
        # Get ICR
        x_ICR_v = -self.v_y / self.omega_z
        x_ICR_left = (veloLeft - self.v_y)/self.omega_z
        x_ICR_right = (veloRight- self.v_y)/self.omega_z
        y_ICR = self.v_x/self.omega_z
        
        self.v_x = (veloRight - veloLeft) * y_ICR / (x_ICR_right - x_ICR_left)
        self.v_y = (veloRight + veloLeft)/2 - (veloRight - veloLeft)/(x_ICR_right - x_ICR_left) * (x_ICR_right+ x_ICR_left)/2
        self.omega_z = (veloRight - veloLeft)/(x_ICR_right - x_ICR_left)
        
        self.v_l = veloLeft
        self.v_r = veloRight
        
        heading = self.roverProperties.heading + self.omega_z * timeStep
        distance = sqrt(self.v_y * self.v_y + self.v_x * self.v_x )
        bearing = atan2(self.v_y, self.v_x)
        
        # Calculate next location
        nextCoordinate = Coordinate.shiftCoordinate(self.roverProperties.position, bearing, distance )
        print("Previous coordinate: " + str(self.roverProperties.position))
        print("Rotational Velocity: " + str(heading))
        print("Next coordinate: " + str(nextCoordinate))
        
        # Update `roverProperties`
        self.roverProperties.position = nextCoordinate
        
        
        
        
        
        
        
        