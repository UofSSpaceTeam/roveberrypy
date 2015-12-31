'''             
Hidden Properties           
'''
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


'''             
Visible Properties           
'''
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
        
        