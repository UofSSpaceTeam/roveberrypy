#TODO:	add outputs to the commands to be sent to the drive process
#		finish goToCommand 
#		add priority to commands so it can be use in priority queue


# --------------------    S I M P L E   H E L P E R S    ----------------------

from math import pi, asin, sqrt, sin, cos, atan2

#haversin formula
def haversin(theta):
    return sin(theta/2)*sin(theta/2)

#******************************************************************************#
#                       C O O R D I N A T E   C L A S S                        #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  #
#   Attributes:                                                                #
#       lat         ::  latitude                                               #
#       lon         ::  longitude                                              #
#       RE          ::  radius of the earth in Poland                          #
#   Member Funcions:                                                           #
#       distanceTo(CoordinateObject)    ::  distance [m] to CoordinateObject   #
#                                           from #self                         #
#       bearingTo(CoordinateObject)     ::  absolute bearing to                #
#                                           CoordinateObject from #self        #
#******************************************************************************#

class Coordinate:
    lat = -1        # latitude in DD
    lon = -1        # longitude in DD
    RE = 6364843    # radius of the earth in poland
    # constuct with longitude and latitude if it exists
    def __init__(self, latitude = -1, longitude = -1, heading = -1):
        self.lat = latitude
        self.lon = longitude
        self.heading = heading
    # get the distance to another coordinate
    def distanceTo(self, coord):
        lat1 = self.lat * pi / 180
        lon1 = self.lon * pi / 180
        lat2 = coord.lat * pi/ 180
        lon2 = coord.lon * pi / 180
        return (2*self.RE*asin( sqrt( haversin(lat2-lat1) +
                                 cos(lat1)*cos(lat2)*haversin(lon2-lon1))))
    # get the bearing to another coordinate
    def bearingTo(self, coord):
        lat1 = self.lat * pi / 180
        lon1 = self.lon * pi / 180
        lat2 = coord.lat * pi/ 180
        lon2 = coord.lon * pi / 180
        bearing = (atan2(sin(lon2-lon1)*cos(lat2),
                         cos(lat1)*sin(lat2)
                         -sin(lat1)*cos(lat2)*cos(lon2-lon1)))
        while(bearing < 0):
            bearing = bearing + 2*pi
        while(bearing > 2*pi):
            bearing = bearing - 2*pi
        return bearing * 180/pi

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  #
#               C O O R D I N A T E S   T E S T   C A S E                      #
#                                                                              #
#   Test case:  distance and bearing from (43.990967, 78.48321) to             #
#               (43.991, 78.4833).                                             #
#   Result:     should be ~8 meters at an absolute bearing of 63[deg]          #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  #

#x = Coordinate(43.990967, 78.48321)
#y = Coordinate(43.991, 78.4833)
#print("Distance from x to y is: ", x.distanceTo(y))
#print("Bearing from x to y is: ", x.bearingTo(y))

#******************************************************************************#
#               E N D   O F   C O O R D I N A T E   C L A S S                  #
#******************************************************************************#








# ---------------    N A V I G A T I O N   C O M M A N D S    ----------------





from abc import ABCMeta, abstractmethod

#******************************************************************************#
# 		C O M M A N D   B A S E   C L A S S 			      				   #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  #
#	Navigation command virtual base class.  			     				   #
#									      									   #	
#	Attributes:	(as of right now just some ideas for some nothing     		   #
#			fancy and feel free to add any others which might be  			   #
#			helpful)					       								   #
#		- All of the attributes should be pretty self-explanatory.    		   #
#									    								       #
#******************************************************************************#


class NavCommand(object):
	__metaclass__ = ABCMeta
	@abstractmethod
	def execute(self):
		pass
	@abstractmethod
	def update(self):
		pass
	@abstractmethod
	def cancel(self):
		pass

		
#*****************************************************************************#
#			E X A M P L E   C O M M A N D                         			  #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#	Prints "I'm suprised someone is actually reading this" 		      		  #
#									      									  #
#	execute			:: 	prints "I'm suprised someone is       				  #
#					actually reading this"		     						  #
#	update(newString) 	::	when execute is called newString will			  #
#					be printed			      								  #
#	cancel			::	make printString empty		      					  #
# 									      									  #
#*****************************************************************************#

class ExampleNavCommand(NavCommand):
	printString = "I'm suprised someone is actually reading this"
	isCancelled = False 
	hasExecuted = False
	def __init__(self, stringToPrint = -1):
		if stringToPrint is not -1:
			self.printString = stringToPrint
		hasExecuted = True
	def execute(self):
		if self.isCancelled is False:
			print(self.printString)
	def update(self, newString):
		self.printString = newString
	def cancel(self):
		self.isCancelled = True
		
		
#*****************************************************************************#
#			F O W A R D   C O M M A N D                         			  #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#	tells the rover to move forward						 		      		  #
#									      									  #
#	execute			:: 	sends a move forward message to the drive       	  #
#						process if not at the target location				  #
#	update(newString) 	::	updates the current coordinate of the rover		  #
#										      								  #
#	cancel			::	stops the command			      					  #
# 									      									  #
#*****************************************************************************#
class ForwardCommand(NavCommand):
	isCancelled = False 
	hasExecuted = False
	def __init__(self, current, target):
		#current and target would be the current coordinate
		self.current = current
		self.target = target
		hasExecuted = True
	def execute(self):
		if self.isCancelled is False:
			#move forward
			pass
	def update(self, newCoordinate):
		self.current = newCoordinate
		if self.current.distanceTo(target) == 2: # or however close you want to get to target 
			self.cancel()
	def cancel(self):
		self.isCancelled = True

#*****************************************************************************#
#				T U R N   C O M M A N D                         			  #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#	tells the rover to turn						 		      		          #
#									      									  #
#	execute			:: 	sends a move message to the drive process for      	  #
#						one side of the rover if not at the target heading	  #
#	update(newString) 	::	updates the current coordinate of the rover		  #
#										      								  #
#	cancel			::	stops the command			      					  #
# 									      									  #
#*****************************************************************************#
class TurnCommand(NavCommand):
	isCancelled = False 
	hasExecuted = False
	def __init__(self, current, target):
		self.current = current
		self.target = target
		hasExecuted = True
	def execute(self):
		if self.isCancelled is False:
			if selfself.current.bearingTo(target) - self.current.heading <= 180:
				#turn right
				pass
			else:
				#turn left
				pass
	def update(self, newCoordinate):
		self.current = newCoordinate
		if abs(self.current.heading - self.current.bearingTo(target)) <= 5:
			self.cancel
	def cancel(self):
		self.isCancelled = True

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#		E X A M P L E   C O M M A N D   T E S T 		      			      #
#	 								      									  #
#	Test case:	test that example command is working properly        		  #
#									   									      #
#	Result:		self explanatory				     						  #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

#example1 = ExampleNavCommand()
#example1.execute()

#example2 = ExampleNavCommand("Hi there")
#example2.execute()

#example3 = ExampleNavCommand()
#example3.update("Print this instead")
#example3.execute()

#example4 = ExampleNavCommand()
#example4.cancel()
#example4.execute() 

#*****************************************************************************#
#		 E N D   O F   E X A M P L E   C O M M A N D		      			  #
#*****************************************************************************#




#*****************************************************************************#
#				DRIVE TO CLASS
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#


class goToCommand(NavCommand):
	destination
	initalBearing = -1
	pathWidth = -1

	def __init__(self, currentCoord, destinationCoord, pathWidth_):
		self.initalBearing = currentCoord.bearingTo(destinationCoord)
		self.pathWidth = pathWidth_
		self.destination = destinationCoord
	def execute(self):
		
		while( initalBearing - currentHeading < 85 ):
			theta = initalBearing - currentHeading
			distFromPath = currentPosition.distanceTo(destination) * sind(theta)
			while(abs(distFromPath) > pathWidth):
				# turn rover