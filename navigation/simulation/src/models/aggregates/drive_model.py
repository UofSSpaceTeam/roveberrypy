from abc import abstractmethod
from models.aggregates import AggregateModel
from math import sqrt, cos, pi, sin, asin, isnan, atan2, degrees, radians
from entities.coordinate import Coordinate
from random import gauss

from copy import deepcopy
from setup.configuration import Configuration


class DriveModel(AggregateModel):
    """ Aggregate model to emulate the driving of the rover.
    
    Attributes:
        MAX_SPEED(float) -- The max speed the rover can drive (ie the speed
                            of the rover when power is full.
    Methods:
        update(timeStep) -- Update the position of the rover after `timeStep`
                            has elapsed.
    """
    
    MAX_SPEED = Configuration.get('rover_model.max_speed')
    RKM = None
    
    def __init__(self, roverModel):
        AggregateModel.__init__(self, roverModel)
        
        KMAConfigPath = 'rover_model.aggregates.drive_model.'
        
        self.roverProperties.powerLeft = Configuration.get('rover_model.initial_conditions.power_left')
        self.roverProperties.powerRight = Configuration.get('rover_model.initial_conditions.power_right')
        
        # Initialize RKM
        KMAInitial = KinematicModel.KMAInit()
        RDPInitial = KinematicModel.RDPInit()
        
        
        # Initialize Kinematic Model Attribute's
        KMAInitial.icr = Configuration.get(KMAConfigPath + 'icr')
        KMAInitial.alpha = Configuration.get(KMAConfigPath + 'alpha')
        
        # Initialize Rover Drive Properties 
        RDPInitial.v_L = self.roverProperties.powerLeft * self.MAX_SPEED
        RDPInitial.v_R = self.roverProperties.powerRight * self.MAX_SPEED
        RDPInitial.position = self.roverProperties.position
        RDPInitial.heading = self.roverProperties.heading
        
        self.RKM = KinematicModel(KMAInitial, RDPInitial)
        
        
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
        v_L = self.roverProperties.powerLeft * self.MAX_SPEED
        v_R = self.roverProperties.powerRight * self.MAX_SPEED
        
        self.RKM.update(v_L, v_R, timeStep)
        
        self.roverProperties.position = self.RKM.position
        self.roverProperties.heading = self.RKM.heading
        
        

  
class KinematicModel(object):
    """ Kinematic model for skid-steer robot.
    
    Attributes:
        vy - X-velocity in the rover relative frame.
        wz - Rotational velocity about Z-axis in relative frame.
        
        v_L - Velocity of the rover's left wheels
        v_R - Velocity of the rover's right wheels
        
        icr - Instantaneous center of rotation for rover's body (relative X-axis)
        
        alpha - Correction factor
        
        position - Reference to rover position.
        heading - Reference to rover heading.
        
        archive - Archive of all atributes.
        
    Classes:
        KMAInit - Data structure for kinematic model attribute initial conditions.
        RDPInit - Data structure for rover drive property initial conditions.
        
    Methods:
        update(dt) -- Update the RKM attributes and calculate the new position.
        All other methods are utility methods.
    """
    # Relative frame kinematics.
    vy = None
    wz = None
    
    # Rover drive properties.
    v_L = None
    v_R = None
    
    # Kinematic model attributes.
    icr = None
    alpha = None
    
    # Rover position attributes.
    position = None
    heading = None
    
    # Model archive.
    archive = None
    
    def __init__(self, KMAInitial, RDPInitial):
        """ Initialize the kinematic model.
        
        Args:
            KMAInitial (KinematicModel.KMAInit) - Initial conditions for 
                                                  kinematic model attributes.
            RDPInitial (KinematicModel.RDPInit) - Initial conditions for 
                                                  rover drive properties.
            RFKInitial (KinematicModel.RFKinit) - Initial conditions for 
                                                  relative frame kinematics.
        """
                
        # Initialize drive properties.
        self.v_L = deepcopy(RDPInitial.v_L)
        self.v_R = deepcopy(RDPInitial.v_R)
        self.position = deepcopy(RDPInitial.position)
        self.heading = deepcopy(RDPInitial.heading)
        
        # Initialize kinematic model attributes.
        self.icr = KMAInitial.icr
        self.alpha = KMAInitial.alpha
        
        self.recalculateRFK()
    
        # Initialize archive.
        self.archive = KinematicModel.Archive()
        
    def archiveState(self):
        """ Utility method: archive the current state of the model."""
        # Archive RFK
        self.archive.vy.append(self.vy)
        self.archive.wz.append(self.wz)
        
        # Archive RDP
        self.archive.v_L.append(self.v_L)
        self.archive.v_R.append(self.v_R)
        
        # Archive KMA
        self.archive.icr.append(self.icr)
        self.archive.alpha.append(self.alpha)
        
        
        self.archive.position.append(deepcopy(self.position))
        self.archive.heading.append(self.heading)
    
    def recalculateRFK(self):
        """ Utility methods: recalculate the relative frame kinematic values """
        # Calculate new RFK values
        self.vy = self.alpha * (self.v_L + self.v_R) / 2.0
        self.wz = self.alpha * (-self.v_L + self.v_R) / (2*self.icr)
        
    
    def updatePosition(self, dt):
        """ Utility methods: update the current position of the rover. """
        distance = self.vy * dt                           # distance moved in dt
        
        # update position and heading
        self.heading = (self.heading - degrees(self.wz * dt))%(360.0)
        self.position = Coordinate.shiftCoordinate(self.position, self.heading, distance)
        
    
    def update(self, v_L, v_R, dt):
        """ Update the kinematic model.
        
        Args:
            v_L - Velocity of left wheels.
            v_R - Velocity of right wheels.
            dt - Elapsed time.
        
        Post:
            All properties and attributes have been updated and archived.
        """
        self.v_L = v_L
        self.v_R = v_R
        self.recalculateRFK()
        self.updatePosition(dt)
        self.archiveState()
    
    class Archive(object):
        """ Utility method: archive the current state of the model. """
        # Relative frame kinematics.
        vy = []
        wz = []
        
        # Rover drive properties.
        v_L = []
        v_R = []
        
        # Kinematic model attributes.
        icr = []
        
        alpha = []
        
        # Rover position attributes.
        position = []
        heading  = []
        
        
    class KMAInit(object):
        """ Data structure for kinematic model attribute initial conditions 
        
        Attributes:
            icr - instantaneous center of rotation
            
            Correction Factors
            -------------------
            alpha
            
        """
        # Initial conditions for kinematic model attributes.
        icr = None
        alpha = None
        
    class RDPInit(object):
        """ Data structure for specifying rover drive property initial 
        conditions and linking rover.properties to model.
        
        Attributes:
            v_L
            v_R
            position - Reference to rover.properties.position
            heading - Reference to rover.properties.heading
        """
        # Initial conditions for rover drive properties.
        v_L = None
        v_R = None
        position = None
        heading = None
    

        
# eof
        