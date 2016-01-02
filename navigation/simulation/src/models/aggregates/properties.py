'''----------------------------------------------------------------------------            
                            RoverProperties           
----------------------------------------------------------------------------'''
class RoverProperties(object):
    def __init__(self, roverModel):
        self._hiddenPriviledge = False
        self._hiddenProperties = roverModel.hiddenProperties
        self._visibleProperties = roverModel.visibleProperties
    
    def grantHiddenAccess(self):
        self._hiddenPriviledge = True
        
    def hasHiddenPriviledge(self):
        return self._hiddenPriviledge
    
    # Hidden Properties
    @property
    def position(self):
        if(self.hasHiddenPriviledge()):
            return self._hiddenProperties.position
        else:
            print("ERROR: Rover property access denied")
    @position.setter 
    def position(self, value):
        if(self.hasHiddenPriviledge()):
            self._hiddenProperties.position = value
        else:
            print("ERROR: Rover property access denied")
    @property
    def heading(self):
        if(self.hasHiddenPriviledge()):
            return self._hiddenProperties.heading
        else:
            print("ERROR: Rover property access denied")
    @property
    def positionLog(self):
        if(self.hasHiddenPriviledge()):
            return self._hiddenProperties.positionLog
        else:
            print("ERROR: Rover property access denied")
    
    # Visible Properties
    @property
    def DESTINATION(self):
        return self._visibleProperties.DESTINATION 
    
    @property
    def powerLeft(self):
        return self._visibleProperties.powerLeft
    @powerLeft.setter 
    def powerLeft(self, value):
        self._visibleProperties.powerLeft = value
        
    @property
    def powerRight(self):
        return self._visibleProperties.powerRight
    @powerRight.setter 
    def powerRight(self, value):
        self._visibleProperties.powerRight = value
        
    @property
    def gpsReadings(self):
        return self._visibleProperties.gpsReadings
    @gpsReadings.setter 
    def gpsReadings(self, value):
        if(self._hiddenPriviledge):
            self._visibleProperties.gpsReadings = value
        else:
            print("ERROR: Rover property access denied")
             
'''----------------------------------------------------------------------------            
                            Hidden Properties           
----------------------------------------------------------------------------'''
class HiddenProperties(object):
    # constructor for hidden model values
    def __init__(self, initialCoordinate, initialHeading):
        self._positionLog = [initialCoordinate]
        self._position = initialCoordinate
        self._heading = initialHeading
    
    # position property. Also handles positionLog and heading
    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, value):
        self._position = value
        self._positionLog.append(value)
        # TODO: call getHeading between two coordinates function
        self._heading = "not yet implemented"
    @property
    def positionLog(self):
        return self._positionLog
    @property
    def heading(self):
        return self._heading
    
    # __str__ method for easy printing hidden values to screen
    def __str__(self):
        return "current position = " + self._position.__str__() + "\nposition log = " + self._positionLog.__str__()


'''----------------------------------------------------------------------------            
                            Visible Properties           
----------------------------------------------------------------------------'''
class VisibleProperties(object):
    # constructor for visible model values
    def __init__(self, DESTINATION):
        self._DESTINATION = DESTINATION
    
    # power to left side
    @property
    def powerLeft(self):
        return self._powerLeft
    @powerLeft.setter 
    def powerLeft(self, value):
        self._powerLeft = value
      
    # power to right side  
    @property
    def powerRight(self):
        return self._powerRight
    @powerRight.setter 
    def powerRight(self, value):
        self._powerRight = value
    
    # gps readings property  
    @property
    def gpsReadings(self):
        return self._gpsReadings
    @gpsReadings.setter 
    def gpsReadings(self, value):
        self._gpsReadings = value
        
    @property
    def DESTINATION(self):
        return self._DESTINATION
        
        