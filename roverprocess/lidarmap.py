from matplotlib import pyplot as plt
import numpy as np
import random
import math
from operator import itemgetter # for LidarMap.partition()
import json
#from lidarimage import plot_result

# TODO: Find some way to associate GPS data with Lidar data.
# TODO: Switch to radians for angle measurements


max_range = 600 # What is considered "infinity"
N = 15 # number of objects to add
max_variance = 15 # How rough can surface of terrain be
width = 1.5
angle_unit = 0.6

class LidarMap():

    def __init__(self, angles, distances):
        self.data = {angle:distance for (angle,distance) in zip(angles, distances)}
        self.update()

    def update(self):
        ''' Update internal data structure.
            This can be time consuming.  '''
        # TODO: optimize?
        self.angles = list(self.data.keys())
        self.angles.sort()
        self.distances = list(self.data.values())
        self.resolution = len(self.angles)
        self.partition()

    def distance(self, angle):
        ''' Returns the distance at the given angle '''
        # TODO: If :angle: is not in our map,
        # interpolate what it should be.
        return self.data[angle]

    def angle_snap(self, angle):
        ''' If :angle: is not in self.data,
            return the angle int self.data
            that is closest to :angle:.
        '''
        if angle in self.data:
            return angle
        else:
            largest_angle = self.angles[len(self.angles) - 1]
            smallest_angle = self.angles[0]
            if abs(largest_angle - angle) > abs(360 + smallest_angle - angle):
                return smallest_angle
            closet = min(range(len(self.angles)), key = lambda i: abs(self.angles[i] - angle))
            return self.angles[closet]

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
        # TODO: is there a __magic__ method that we can define
        # so that we can use pythons slice syntax? ( my_list[2:5] )
        # TODO: What should we do if end < start?
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

    def previous(self, angle):
        ''' Same as next, but for the previous angle'''
        if angle in self.data:
            i = self.angles.index(angle)
            if i == 0:
                return self.angles[-1]
            else:
                return self.angles[i - 1]

    def partition(self):
        ''' Divides map into sections by finding points that undergo a
            sharp change in distance, indicating the possibility
            of object boundries.
        '''
        # TODO: optimize?
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
            self.deleteHoles()
        else:
            self.partitions = []
    
    def deleteHoles(self):
        '''delete partitions that is smaller than the width of rover, which rover could not pass through'''
        holes = self.findHoles()
        if len(holes) > 0:
            holes = self.mergeMultipleHoles(holes)
            if holes is not None:
                partitions = []
                i = 0
                if holes[-1][0] > holes[-1][1]:
                    i = holes[-1][1] + 1
                j = 0
                while i < len(self.partitions):
                    if i == holes[j][0]:
                        k = holes[j][1]
                        partitions.append((self.partitions[i][0], self.partitions[k][1], self.partitions[i][2]))
                        if holes[j][0] > k:
                            break
                        j = j + 1
                        i = k + 1
                    else:
                        partitions.append(self.partitions[i])
                        i = i + 1
                self.partitions = partitions
    
    def mergeMultipleHoles(self, holes):
        if len(holes) <= 1:
            return holes
        result = []
        i = 0
        this = holes[0]
        while i < len(holes):
            next = holes[i + 1]
            if this[1] != next[0]:
                result.append(this)
                this = next
            else:
                this = (this[0], next[1])
            i = i + 1
        if len(result) > 0:
            if this[1] == result[0][0]:
                result[0] = (this[0],result[0][1])
            else:
                result.append(this)
        else:
            if this[0] == this[1]:
                self.partitions = []
                return None
            else:
                result.append(this)
        return result
        
    def findHoles(self):
        holes = []
        for i in range(0, len(self.partitions)):
            this = self.partitions[i]
            angle = width / this[2]
            if angle > angle_unit:
                left_angle = (this[0] - angle) % 360
                
                right_angle = (this[1] + angle) % 360
                
                left = self.findPartition(left_angle)
                right = self.findPartition(right_angle)
                left_hole_candidate = findPartitionsInBetween(left, i)
                right_hole_candidate = findPartitionsInBetween(i, right)
                if left_hole_candidate is not None and abs(this[2] - self.partitions[left][2]) < 2*max_variance:
                    isHole = True
                    for j in left_hole_candidate:
                        if self.partitions[j][2] < this[2]:
                            isHole = False
                            break
                    if isHole:
                        holes.append((left, i))
                if right_hole_candidate is not None and abs(this[2] - self.partitions[right][2]) < 2*max_variance:
                    isHole = True
                    for j in right_hole_candidate:
                        if self.partitions[j][2] < this[2]:
                            isHole = False
                            break
                    if isHole:
                        holes.append((i,right))
        return holes
                
                
    def findPartitionsInBetween(self, i, j):
        ''' find the index of all partitions between partition[i] and partition[j]'''
        if i + 1 == j:
            return None
        elif i < j:
            return range(i+1, j)
        elif i == len(self.partitions) - 1 and j == 0:
            return None
        else:
            return range(i - len(self.partitions)+1, j)


    def findPartition(self, angle):
        ''' Find the partition that the input angle belongs to
        '''
        if self.partitions == []:
            raise RuntimeError()
        else:
            for i in range(len(self.partitions) - 1):
                partition = self.partitions[i]
                if angle > partition[0] and angle < partition[1]:
                    return i
            i = len(self.partitions) - 1
            partition = self.partitions[i]
            if angle > partition[0] or angle < partition[1]:
                return i

    def findNextPartition(self, i):
        if i < len(self.partitions) - 1:
            return i + 1
        else:
            return 0

    def findPreviousPartition(self, i):
        if i == 0:
            return len(self.partitions) - 1
        else:
            return i - 1

    def find_farthest_region(self):
        ''' Find region that farthest away from us,
            and store a version of the partition map
            sorted farthest to closest.
        '''
        if self.partitions == []:
            raise RuntimeError()
        self.by_farthest = sorted(self.partitions, key=itemgetter(2), reverse=True)[0]
        return self.by_farthest[0], self.by_farthest[1]

    def find_closest_region(self):
        ''' Finds the region that is closest to us,
            and store a version of the partition map
            sorted closest to farthest.
        '''
        if self.partitions == []:
            raise RuntimeError()
        self.by_closest = sorted(self.partitions, key=itemgetter(2), reverse=False)[0]
        return self.by_closest[0], self.by_closest[1]

    def find_opening(self, angle):
        ''' Find the closet partition that is more far than the partition in the target angle
        '''
        if self.partitions == []:
            raise RuntimeError()
        else:
            i = self.findPartition(angle)
            partition = self.partitions[i]
            if (angle - partition[0]) % 360 < (partition[1] - angle) % 360:
                previous = self.findPreviousPartition(i)
                pre_partition = self.partitions[previous]
                if partition[2] > pre_partition[2]:
					
                    return self.angle_snap((partition[0] - width / partition[2])%360), pre_partition[2]
                else:
                    return self.angle_snap((pre_partition[1]+width / pre_partition[2])%360), partition[2]
            else:
                next = self.findNextPartition(i)
                next_partition = self.partitions[next]
                if partition[2] > next_partition[2]:
                    return self.angle_snap((partition[1]+width / partition[2])%360, next_partition[2]
                else:
                    return self.angle_snap((next_partition[0]-width / next_partition[2])%360, partition[2]

######################################
######## END class LidarMap ##########
######################################


def center(angle_start, angle_end):
    """ Find the center of an angle."""
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

        # How much to vary the object surface by
        roughness = random.randrange(1,max_variance)

        length = end-start
        # Add object while varying the surface
        # TODO: All these segments are concave, most of the terrain
        # we encounter will be convex.
        # TODO: Generate rectangular shaped (man made) objects?
        for j in m.slice(start,end):
            m.set_point(j, obj_dist+random.randrange(-roughness,roughness), do_update=False)
    m.update()
    return m

def export_map(m, pathname):
    """ Export a lidar map to a csv file
        (Maybe point cloud?) """
    f = open(pathname, 'w')
    cart = map_to_cartesian(m, (0,0))
    # for p in cart:
    #     f.write("{} {}\n".format(p[0], p[1]))
    json.dump(cart, f)


def import_map(pathname):
    """ Read a map from disk"""
    f = open(pathname, 'r')
    cart = json.load(f)
    return cartesian_to_map(cart, (0,0))

def map_to_cartesian(m, origin):
    """ Takes points stored in a LidarMap and returns
        a list of the points converted to cartesian coordinates
        offset from the origin where the LidarMap is taken from.
    """
    return [(m.distance(a)*math.cos(a)+origin[0],
        m.distance(a)*math.sin(a)+origin[1]) for a in m.angles]

def cartesian_to_map(cart, origin):
    angles = []
    distances = []
    for p in cart:
        a = math.atan2(origin[1]-p[1], origin[0]-p[0])
        d = math.sqrt((origin[0]-p[0])**2 + (origin[1]-p[1])**2)
        if a < 0:
            a += 2*math.pi
        angles.append(int(math.degrees(a)))
        distances.append(d)
    return LidarMap(angles, distances)

def PathFinding(target, m):
    waypoints = [(0,0)]

    # First check if we can see the position
    if target[1] < m.distance(m.angle_snap(target[0])):
        waypoints.append(target)
        # target within view exit early
        #plot_result(m, waypoints, target)
    else:
        opening = m.find_opening(target[0])
        if opening is not None:
            waypoints.append(opening)
            #plot_result(m, waypoints, target)
        else:
            # Assume we are in a corner or cave, and try
            # to get away from the obsticals
            deep_angle = center(*m.find_farthest_region())
            waypoints.append((deep_angle, max_range))
    return waypoints
            

def main():
    ''' Path finding algorithm.'''
    target = (random.randrange(0,360),
                    random.randrange(max_range/2,max_range))
    m = gen_map()
    waypoints = PathFinding(target, m)
    plot_result(m, waypoints, target)

if __name__ == '__main__':
    m = gen_map()
    export_map(m, "output.json")
    m1 = import_map("output.json")
    for a in m.angles:
        if a not in m1.angles:
            print(a)
    print(m1.angles)

    # from test import test_lidarmap
    # test_lidarmap()
