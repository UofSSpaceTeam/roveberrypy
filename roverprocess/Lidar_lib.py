from matplotlib import pyplot as plt
import numpy as np
import random
import math
from operator import itemgetter # for LidarMap.partition()


max_range = 600
N = 15 # number of objects to add
max_variance = 15

class LidarMap():

    def __init__(self, angles, distances):
        self.data = {angle:distance for (angle,distance) in zip(angles, distances)}
        self.update()

    def update(self):
        ''' Update internal data structure.
            This can be time consuming.  '''
        self.angles = list(self.data.keys())
        self.angles.sort()
        self.distances = list(self.data.values())
        self.resolution = len(self.angles)
        self.partition()

    def distance(self, angle):
        return self.data[angle]

    def set_point(self, angle, distance, do_update=True):
        ''' Add a new data point or update an existing one.
            By default it calls update, so if you are making
            lots of changes at once, call with do_update=False
            and remember to call LidarMap.update() once you're
            done calling set_point()
        '''
        should_update = do_update and (angle not in self.data \
                or self.distance(angle) != distance)
        self.data[angle] = distance
        if should_update:
            self.update()

    def slice(self, start, end):
        ''' Returns a list of all angles in the range start to end '''
        seg = []
        for a in list(self.data.keys()):
            if start <= a <= end:
                seg.append(a)
        return seg

    def next(self, angle):
        ''' Returns the next angle after the given one.
            This is needed because the lidar map won't necessarily
            have an entry for angle+1.
        '''
        if angle in self.data:
            i = self.angles.index(angle)
            if i == len(self.angles)-1:
                i = 0
            else:
                i += 1
            return self.angles[i]

    def partition(self):
        ''' Divides map into sections by finding points that undergo a
            sharp change in distance, indicating the possibility
            of object boundries.
        '''
        self.edges = []
        for x in self.slice(0,359):
            a = self.distance(x)
            b = self.distance(self.next(x))
            if(abs(b-a) > 2*max_variance):
                self.edges.append(x)

        if self.edges != []:
            self.partitions = [(self.edges[i], self.edges[i+1], self.distance(self.edges[i+1]))
                    for i in range(0, len(self.edges)-1, 1)]
            self.partitions.append((self.edges[-1], self.edges[0],
                self.distance(self.edges[0])))
        else:
            self.partitions = []

    def find_farthest_region(self):
        ''' Find region that farthest away from us,
            and store a version of the partition map
            sorted farthest to closest.
        '''
        self.by_farthest = sorted(self.partitions, key=itemgetter(2), reverse=True)[0]
        return self.by_farthest[0], self.by_farthest[1]

    def find_closest_region(self):
        ''' Finds the region that is closest to us,
            and store a version of the partition map
            sorted closest to farthest.
        '''
        self.by_closest = sorted(self.partitions, key=itemgetter(2), reverse=False)[0]
        return self.by_closest[0], self.by_closest[1]

def center(angle_start, angle_end):
    """ Find the center of a partition"""
    if angle_start > angle_end:
        angle = (angle_end+360+angle_start)/2
        if angle >= 360:
            angle -= 360
    else:
        angle = (angle_end+angle_start)/2
    return angle

def gen_map():
    ''' Generates a randomized LidarMap.
        'Objects' are placed at random positions, and
        have rough surfaces to simulate rocky terrain
    '''
    m = LidarMap(list(range(0,360)), [max_range]*360)
    # add up to N objects (at least 1)
    for i in range(0,random.randrange(1,N)):
        a = random.randrange(0,360)
        b = random.randrange(0,360)
        start = min(a,b)
        end = max(a,b)

        # Object is located approximately here
        obj_dist = random.randrange(2*max_variance,max_range)

        # how much to vary the object surface by
        roughness = random.randrange(1,max_variance)

        length = end-start
        # Add object while varying the surface
        for j in m.slice(start,end):
            m.set_point(j, obj_dist+random.randrange(-roughness,roughness), do_update=False)
    m.update()
    return m


def plot_result(m, waypoints, target):
    """ Plot the map and waypoints with matplotlib"""
    angles = np.linspace(0,np.pi*2, m.resolution)
    way_angles = [angles[int(a)] for a in list(zip(*waypoints))[0]]
    way_dists = list(zip(*waypoints))[1]

    plt.polar(angles, m.distances, 'k',# terrain
              way_angles, way_dists,'r', #path
              angles[target[0]], target[1], 'go')
    plt.show()

def plot_map(m):
    ''' Plots the lidar map with matplotlib'''
    angles = [math.radians(x) for x in m.angles]
    plt.polar(angles, m.distances)
    plt.show()

def main():
    ''' Path finding algorithm.'''
    target = (random.randrange(0,360),
                    random.randrange(max_range/2,max_range))
    m = gen_map()
    waypoints = [(0,0)]

    # First check if we can see the position
    for x in range(0,360):
        if x == target[0] and target[1] < m.distance(x):
            waypoints.append(target)
            # target within view exit early
            plot_result(m, waypoints, target)
            return

    deep_angle = center(*m.find_farthest_region())
    waypoints.append((deep_angle, max_range))

    plot_result(m, waypoints, target)

if __name__ == '__main__':
    main()
