from math import floor
class TimeStamp(object):
    """ A class to represent a time.
    
    Methods:
        __add__(self, otherInstance) -- Add two times (+ operator)
        __sub__(self, otherInstance) -- Add two times (- operator)
        __str__(self) -- Convert to string.
    Static Methods:
        toSeconds() -- Get the time in seconds.
    """
    def __init__(self, hours, minutes, seconds):
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds
    
    @property
    def hours(self):
        return self._hours
    @hours.setter 
    def hours(self, value):
        self._hours = value
    @property
    def minutes(self):
        return self._minutes
    @minutes.setter 
    def minutes(self, value):
        self._minutes = value
    @property
    def seconds(self):
        return self._seconds
    @seconds.setter
    def seconds(self, value):
        self._seconds = value
        
    def __add__(self, other):
        seconds = self.seconds + other.seconds
        minutes = self.minutes + other.minutes + floor(seconds/60)
        hours = self.hours + other.hours + floor(minutes/60)
        return TimeStamp(hours, minutes % 60, seconds % 60)
    
    def __sub__(self, other):
        seconds = self.seconds
        minutes = self.minutes
        hours = self.hours
        if(seconds < other.seconds):
            seconds = seconds + 60
            minutes = minutes - 1
        if(minutes < other.minutes):
            minutes = minutes + 60
            hours = hours - 1
        hours = hours - other.hours
        minutes = minutes - other.minutes
        seconds = seconds - other.seconds
        return TimeStamp(hours, minutes, seconds)
    
    def __str__(self):
        return str(self.hours) + ":" + str(self.minutes) + ":" + str(self.seconds)  
    
    @staticmethod
    def toSeconds(time):
        return time.hours * 3600 + time.minutes * 60 + time.seconds
        