from abc import abstractmethod
from models.aggregates import AggregateModel
from math import sqrt, cos, pi, sin, asin, isnan, atan2
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
        RFKInitial = KinematicModel.RFKInit()
        
        
        # Initialize Kinematic Model Attribute's
        KMAInitial.icr_Vx = Configuration.get(KMAConfigPath + 'icr_vx')
        KMAInitial.icr_Lx = Configuration.get(KMAConfigPath + 'icr_lx')
        KMAInitial.icr_Rx = Configuration.get(KMAConfigPath + 'icr_rx')
        KMAInitial.icr_Vy = Configuration.get(KMAConfigPath + 'icr_vy')
        KMAInitial.icr_Ly = Configuration.get(KMAConfigPath + 'icr_ly')
        KMAInitial.icr_Ry = Configuration.get(KMAConfigPath + 'icr_ry')
        KMAInitial.alpha_L = Configuration.get(KMAConfigPath + 'alpha_l')
        KMAInitial.alpha_R = Configuration.get(KMAConfigPath + 'alpha_r')
        
        # Initialize Rover Drive Properties 
        RDPInitial.v_L = Configuration.get(KMAConfigPath + 'v_l')
        RDPInitial.v_R = Configuration.get(KMAConfigPath + 'v_l')
        RDPInitial.position = self.roverProperties.position
        RDPInitial.heading = self.roverProperties.heading
        
        # Initialize Relative Frame Kinematics
        RFKInitial.vx = Configuration.get(KMAConfigPath + 'vx')
        RFKInitial.vy = Configuration.get(KMAConfigPath + 'vy')
        RFKInitial.wz = Configuration.get(KMAConfigPath + 'wz')
        
        self.RKM = KinematicModel(KMAInitial, RDPInitial, RFKInitial)
        
        
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
        vy - Y-velocity in the rover relative frame.
        vx - X-velocity in the rover relative frame.
        wz - Rotational velocity about Z-axis in relative frame.
        
        v_L - Velocity of the rover's left wheels
        v_R - Velocity of the rover's right wheels
        
        icr_Vx - Instantaneous center of rotation for rover's body (relative X-axis)
        icr_Vy - Instantaneous center of rotation for rover's body (relative Y-axis)
        icr_Lx - Instantaneous center of rotation for left side (relative X-axis)
        icr_Ly - Instantaneous center of rotation for left side (relative Y-axis)
        icr_Rx - Instantaneous center of rotation for right side (relative X-axis)
        icr_Ry - Instantaneous center of rotation for for right side (relative Y-axis)
        
        alpha_L - Correction factor for left side
        alpha_R - Correction factor for right side
        
        position - Reference to rover position.
        heading - Reference to rover heading.
        
        archive - Archive of all atributes.
        
    Classes:
        KMAInit - Data structure for kinematic model attribute initial conditions.
        RDPInit - Data structure for rover drive property initial conditions.
        RFKInit - Data structure for relative frame kinematics initial conditions. 
        
    Methods:
        update(dt) -- Update the RKM attributes and calculate the new position.
        All other methods are utility methods.
    """
    # Relative frame kinematics.
    vx = None
    vy = None
    wz = None
    
    # Rover drive properties.
    v_L = None
    v_R = None
    
    # Kinematic model attributes.
    icr_Vx = None
    icr_Lx = None
    icr_Rx = None
    icr_Vy = None
    icr_Ly = None
    icr_Ry = None
    
    alpha_R = None
    alpha_L = None
    
    # Rover position attributes.
    position = None
    heading = None
    
    # Model archive.
    archive = None
    
    def __init__(self, KMAInitial, RDPInitial, RFKInitial):
        """ Initialize the kinematic model.
        
        Args:
            KMAInitial (KinematicModel.KMAInit) - Initial conditions for 
                                                  kinematic model attributes.
            RDPInitial (KinematicModel.RDPInit) - Initial conditions for 
                                                  rover drive properties.
            RFKInitial (KinematicModel.RFKinit) - Initial conditions for 
                                                  relative frame kinematics.
        """
        # Initialize relative frame kinematics.
        self.vx = RFKInitial.vx
        self.vy = RFKInitial.vy
        self.wz = RFKInitial.wz
        
        # Initialize drive properties.
        self.v_L = RDPInitial.v_L
        self.v_R = RDPInitial.v_R
        self.position = RDPInitial.position
        self.heading = RDPInitial.heading
        
        # Initialize kinematic model attributes.
        self.icr_Vx = KMAInitial.icr_Vx
        self.icr_Lx = KMAInitial.icr_Lx
        self.icr_Rx = KMAInitial.icr_Rx
    
        self.icr_Vy = KMAInitial.icr_Vy
        self.icr_Ly = KMAInitial.icr_Ly
        self.icr_Ry = KMAInitial.icr_Ry
        
        self.alpha_L = KMAInitial.alpha_L
        self.alpha_R = KMAInitial.alpha_R
    
        # Initialize archive.
        self.archive = KinematicModel.Archive()
        
    def archiveState(self):
        """ Utility method: archive the current state of the model."""
        # Archive RFK
        self.archive.vx.append(self.vx)
        self.archive.vy.append(self.vy)
        self.archive.wz.append(self.wz)
        
        # Archive RDP
        self.archive.v_L.append(self.v_L)
        self.archive.v_R.append(self.v_R)
        
        # Archive KMA
        self.archive.icr_Vx.append(self.icr_Vx)
        self.archive.icr_Lx.append(self.icr_Lx)
        self.archive.icr_Rx.append(self.icr_Rx)
        self.archive.icr_Vy.append(self.icr_Vy)
        self.archive.icr_Ly.append(self.icr_Ly)
        self.archive.icr_Ry.append(self.icr_Ry)
        self.archive.alpha_L.append(self.alpha_L)
        self.archive.alpha_R.append(self.alpha_R)
        self.archive.position.append(deepcopy(self.position))
        self.archive.heading.append(deepcopy(self.position))
        
    def recalculateKMA(self):
        """ Utility method: recalculate the kinematic model attributes """
        # Calculate new KMA
        self.icr_Vx = -self.vy/self.wz
        self.icr_Lx = (self.alpha_L*self.v_L - self.vy)/self.wz
        self.icr_Rx = (self.alpha_R*self.v_R - self.vy)/self.wz
        self.icr_Vy = self.vx/self.wz
        self.icr_Ly = self.vx/self.wz
        self.icr_Ry = self.vx/self.wz
    
    def recalculateRFK(self):
        """ Utility methods: recalculate the relative frame kinematic values """
        # Calculate new RFK values
        coeff = 1.0/(self.icr_Rx - self.icr_Lx)
        self.vx = coeff * self.icr_Vy * ( -self.alpha_L*self.v_L + self.alpha_R*self.v_R)
        self.vy = coeff * ( self.icr_Rx*self.alpha_L*self.v_L - self.icr_Lx*self.alpha_R*self.v_R)
        self.wz = coeff * ( -self.alpha_L*self.v_L + self.alpha_R*self.v_R)
    
    def updatePosition(self, dt):
        """ Utility methods: update the current position of the rover. """
        v = sqrt(self.vx*self.vx + self.vy*self.vy) # current velocity
        distance = v * dt                           # distance moved in dt
        moveBearing = self.heading + atan2(self.vx, self.vy)       # the bearing of the movement
        
        # update position and heading
        self.position = Coordinate.shiftCoordinate(self.position, moveBearing, distance)
        self.heading = self.heading + self.wz * dt
        
        
    
    def update(self, v_L, v_R, dt):
        """ Update the kinematic model.
        
        Args:
            v_L - Velocity of left wheels.
            v_R - Velocity of right wheels.
            dt - Elapsed time.
        
        Post:
            All properties and attributes have been updated and archived.
        """
        self.recalculateKMA()
        self.recalculateRFK()
        self.updatePosition(dt)
        self.archiveState()
    
    class Archive(object):
        """ Utility method: archive the current state of the model. """
        # Relative frame kinematics.
        vx = []
        vy = []
        wz = []
        
        # Rover drive properties.
        v_L = []
        v_R = []
        
        # Kinematic model attributes.
        icr_Vx = []
        icr_Lx = []
        icr_Rx = []
        icr_Vy = []
        icr_Ly = []
        icr_Ry = []
        alpha_R = []
        alpha_L = []
        
        # Rover position attributes.
        position = []
        heading  = []
        
        
    class KMAInit(object):
        """ Data structure for kinematic model attribute initial conditions 
        
        Attributes:
            Instantaneous Center of Rotation Coordinates
            ---------------------------------------------
            icr_Vx
            icr_Vy
            icr_Lx
            icr_Ly
            icr_Rx
            icr_Ry
            
            Correction Factors
            -------------------
            alpha_L
            alpha_R
        """
        # Initial conditions for kinematic model attributes.
        icr_Vx = None
        icr_Lx = None
        icr_Rx = None
        icr_Vy = None
        icr_Ly = None
        icr_Ry = None
        alpha_L = None
        alpha_R = None
        
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
        
    class RFKInit(object):
        """ Data structure for specifying relative frame kinematic values.
        
        Attributes:
            vx
            vy
            wz
        """
        # Initial conditions for relative frame kinematics.
        vx = None
        vy = None
        wz = None
    
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        