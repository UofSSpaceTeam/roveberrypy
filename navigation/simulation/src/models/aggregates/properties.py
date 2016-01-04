from entities.coordinate import Coordinate
class RoverProperties(object):
    """ Object which handles the properties of RoverModel.
    
    Methods:
        grantHiddenAccess() -- give this instance hidden access
        hasHiddenAccess() -- check if this instance has hidden access
    
    Note:
        Properties are either hidden or visible. This class is used to enforce
        this priviledges
        
    Exception's:
        AttributeError -- thrown when access priviledge is not satisfied.
    """
    
    
    def __init__(self, roverModel):
        """ Construct link to `roverModel.hiddenProperties` and 
        `roverModel.visibleProperties`.
        
        Default:
            By default an instance has visible property access priviledge only.
        """
        self._hiddenPriviledge = False
        self._hiddenProperties = roverModel.hiddenProperties
        self._visibleProperties = roverModel.visibleProperties
    
    def grantHiddenAccess(self):
        """ Give `self` hidden property priviledge """
        self._hiddenPriviledge = True
        
    def hasHiddenPriviledge(self):
        """ Check if `self` has hidden priviledge """
        return self._hiddenPriviledge
    
    # Hidden Properties
    @property
    def position(self):
        """ The correct position of the rover in the simulation. 
        
        Access:
            - Hidden
            
        Note:
            When position is set `positionLog` and `heading` are also updated. 
        """
        if(self.hasHiddenPriviledge()):
            return self._hiddenProperties.position
        else:
            raise AttributeError("Access to `RoverModel.hiddenProperties` was denied.")
    @position.setter 
    def position(self, value):
        if(self.hasHiddenPriviledge()):
            self._hiddenProperties.position = value
        else:
            raise AttributeError("Access to `RoverModel.hiddenProperties` was denied.")
    @property
    def heading(self):
        """ The current heading of the rover.
        
        Access:
            - Hidden
        Note:
            This property does not have a setter. It is set when `position` is updated.
        """
        if(self.hasHiddenPriviledge()):
            return self._hiddenProperties.heading
        else:
            raise AttributeError("Access to `RoverModel.hiddenProperties` was denied.")
    @property
    def positionLog(self):
        """ A log of the position of the rover.
        
        Access:
            - Hidden
        Note:
            This property does not have a setter. It is updated with `position`.
        """
        if(self.hasHiddenPriviledge()):
            return self._hiddenProperties.positionLog
        else:
            raise AttributeError("Access to `RoverModel.hiddenProperties` was denied.")
    
    # Visible Properties
    @property
    def DESTINATION(self):
        """ The destination of the rover.
        
        Access:
            - Visible
        Note:
            This property does not have a setter. It is constant and set in
            `RoverModel.__init__`.
        """
        return self._visibleProperties.DESTINATION 
    
    @property
    def powerLeft(self):
        """ The power to the left side of the rover. 
        
        Access:
            - Visible
        """
        return self._visibleProperties.powerLeft
    @powerLeft.setter 
    def powerLeft(self, value):
        self._visibleProperties.powerLeft = value
        
    @property
    def powerRight(self):
        """ The power to the left side of the rover. 
        
        Access:
            - Visible
        """
        return self._visibleProperties.powerRight
    @powerRight.setter 
    def powerRight(self, value):
        self._visibleProperties.powerRight = value
        
    @property
    def gpsReading(self):
        """ The most recent GPS reading of the rover.
        
        Access:
            getter -- Visible
            setter -- Hidden
        Note:
            This property can only be set when `self` has hidden access.
        """
        return self._visibleProperties.gpsReading
    @gpsReading.setter 
    def gpsReading(self, value):
        if(self._hiddenPriviledge):
            self._visibleProperties.gpsReading = value
        else:
            raise AttributeError("Access to `RoverModel.hiddenProperties` was denied.")
             

class HiddenProperties(object):
    """ The hidden properties of RoverModel
    
    For description see `RoverProperties`
    """
    def __init__(self, initialCoordinate, initialHeading):
        self._positionLog = [initialCoordinate]
        self._position = initialCoordinate
        self._heading = initialHeading
    
    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, value):
        self._heading = Coordinate.getBearing(self.position, value)
        self._position = value
        self._positionLog.append(value)
        
    @property
    def positionLog(self):
        return self._positionLog
    
    @property
    def heading(self):
        return self._heading


class VisibleProperties(object):
    """ The visible properties of RoverModel
    
    For description see `RoverProperties`
    """
    def __init__(self, DESTINATION):
        self._DESTINATION = DESTINATION
    
    
    @property
    def powerLeft(self):
        return self._powerLeft
    @powerLeft.setter 
    def powerLeft(self, value):
        self._powerLeft = value
      
     
    @property
    def powerRight(self):
        return self._powerRight
    @powerRight.setter 
    def powerRight(self, value):
        self._powerRight = value
    
      
    @property
    def gpsReading(self):
        return self._gpsReading
    @gpsReading.setter 
    def gpsReading(self, value):
        self._gpsReading = value
        
    @property
    def DESTINATION(self):
        return self._DESTINATION
        
        