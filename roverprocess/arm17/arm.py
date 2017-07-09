import collections
import math
import time
from enum import Enum

""" Container used to associate a value with each joint of the arm.
"""
Joints = collections.namedtuple('Joints', [
    'base',
    'shoulder',
    'elbow',
    'wrist_pitch',
    'wrist_roll',
    'gripper'
])

""" Container used to associate a value with each static member of the arm.
"""
Sections = collections.namedtuple('Sections', [
    'upper_arm',
    'forearm',
    'end_effector'
])

""" Container used to express a position in cylindrical coordinates
"""
CylindricalCoordinate = collections.namedtuple('CylindricalCoordinate', [
    'r', 'theta', 'z'
])


def make_max_1(tup):
    """ Linearly scale all value in a tuple such that the max magnitude is 1.

    :param tup: The tuple.
    :return: Scaled version of tup where max magnitude is 1.
    """
    max_value = abs(max(max(tup), -min(tup)))
    normed = [0] * len(tup)
    if max_value != 0:
        for i in range(len(tup)):
            normed[i] = tup[i] / max_value
    return tuple(normed)

def tuple_x_tuple(tup1, tup2):
    """ Element-wise multiplication of tuples.

    :param tup1: Tuple 1
    :param tup2: Tuple 2
    :return: Element-wise multiplication of tuples.
    """
    v = [0] * len(tup1)
    for i in range(len(tup1)):
        v[i] = tup1[i] * tup2[i]
    return tuple(v)


class Limits(collections.namedtuple('Limits', 'lower upper')):
    """ Used to specify a joint's limits.

    :units: radians
    :measurement: Limit is measured value (ie relative to longitudinal axis of previous section)
    """

    def is_valid(self, pos, speed):
        """ Check if the given parameters satisfy this joints limit.

        :param pos: Position of joint [radians]
        :param speed: Speed of the joint[radians/s]
        :return: True if speed is valid.
        """
        if self.lower < pos and pos < self.upper:
            return True
        elif pos < self.lower and speed > 0:
            return True
        elif pos > self.upper and speed < 0:
            return True
        else:
            return False

    @staticmethod
    def enforce(limits, pos, speed):
        adjusted = [0] * len(speed)
        for i in range(len(limits)):
            if limits[i] and not limits[i].is_valid(pos[i], speed[i]):
                adjusted[i] = 0
            else:
                adjusted[i] = speed[i]
        return tuple(adjusted)


class Config:
    def __init__(self, section_lengths, joint_limits, max_angular_velocity):
        ''' Create a new arm configuration.
            :param section_lengths (Sections): Lengths of each arm section in meters.
            :param joint_limits (Joints): Rotation limits of each joint in radians.
            :param max_angular_velocity (Joints): Maximum rotational speed of each joint
                                                  in radians/second.
        '''
        self.section_lengths = section_lengths
        self.joint_limits = joint_limits
        self.max_angular_velocity = max_angular_velocity


class Geometry:
    """ A class which calculates the current geometry of the arm from joint measurements.
    """

    def __init__(self, section_lengths, joint_positions):
        absolute_angles = Joints (
            joint_positions.base,
            joint_positions.shoulder,
            joint_positions.elbow + joint_positions.shoulder,
            joint_positions.wrist_pitch + joint_positions.elbow + joint_positions.shoulder,
            None,
            None
        )
        # get convenient variables
        l0 = section_lengths.upper_arm
        l1 = section_lengths.forearm + section_lengths.end_effector
        phi0 = absolute_angles.shoulder
        phi1 = absolute_angles.elbow
        # compute position
        r = l0 * math.sin(phi0) + l1 * math.sin(phi1)
        z = l0 * math.cos(phi0) + l1 * math.cos(phi1)
        self.position = CylindricalCoordinate(r, joint_positions.base, z)
        # compute position gradient
        self.dr = (l0 * math.cos(phi0) + l1 * math.cos(phi1), l1 * math.cos(phi1))
        self.dz = (-l0 * math.sin(phi0) -l1 * math.sin(phi1), -l1 * math.sin(phi1))

    def hold_radius(self):
        """ Used to move along the vertical axis.

        :return: Speed ratio's such that radius is constant.
        """
        delta_phi0 = -self.dr[1] / self.dr[0]
        delta_phi1 = 1
        if self.dr[0] * delta_phi0 + self.dr[1] * delta_phi1 < 0:
            delta_phi0 *= -1
            delta_phi1 *= -1
        return make_max_1((delta_phi0, delta_phi1))

    def hold_altitude(self):
        """ Used to move along the horizontal axis.

        :return: Speed ratio's such that altitude is constant.
        """
        delta_phi0 = -self.dz[1] / self.dz[0]
        delta_phi1 = 1
        if self.dz[0] * delta_phi0 + self.dz[1] * delta_phi1 < 0:
            delta_phi0 *= -1
            delta_phi1 *= -1
        return make_max_1((delta_phi0, delta_phi1))

    def maintain_wrist_pitch(self, d_shoulder, d_elbow):
        """ Used to hold the wrist pitch constant during a planar movement.

        :param d_shoulder: Speed of the shoulder [radians/s]
        :param d_elbow: Speed of the elbow [radians/s]
        :return: Speed of the wrist_pitch [radians/s]
        """
        return -d_shoulder - d_elbow


class ControlMode:
    def __call__(self, config, joints, *user_args):
        raise NotImplementedError()


class ManualControl:
    def __call__(self, config, joints, geometry, base, shoulder, elbow, wrist_pitch, wrist_roll, gripper):
        speed = Joints(
            *tuple_x_tuple(
                config.max_angular_velocity,
                (base, shoulder, elbow, wrist_pitch, wrist_roll, gripper)
            )
        )
        speed = Limits.enforce(config.joint_limits, joints, speed)
        return speed


class PlanarControl:
    def __call__(self, config, joints, geometry, dr, dz, base, wrist_pitch, wrist_roll, gripper):
        # calculate planar movement
        drp0, drp1 = geometry.hold_radius() # 1, 0.832
        dzp0, dzp1 = geometry.hold_altitude()
        shoulder, elbow = (dz * drp0 + dr * dzp0, dz * drp1+ dr * dzp1)
        wrist_pitch += geometry.maintain_wrist_pitch(shoulder, elbow)
        if abs(wrist_pitch) > 1:
            wrist_pitch = wrist_pitch / abs(wrist_pitch)
        shoulder, elbow, wrist_pitch = make_max_1((shoulder, elbow, wrist_pitch))
        speed = Joints(
            *tuple_x_tuple(
                config.max_angular_velocity,
                (base, shoulder, elbow, wrist_pitch, wrist_roll, gripper)
            )
        )
        speed = Limits.enforce(config.joint_limits, joints, speed)

        # if shoulder or elbow are at the limit then we want to halt movement
        if not config.joint_limits.shoulder.is_valid(joints.shoulder, speed[1]):
            new_speed = list(speed)
            new_speed[2] = 0 # elbow
            speed = tuple(new_speed)
        if not config.joint_limits.elbow.is_valid(joints.elbow, speed[2]):
            new_speed = list(speed)
            new_speed[1] = 0 # elbow
            speed = tuple(new_speed)
        return speed


class Controller:
    # constant members
    _config = None

    # variable members
    _control_mode = None
    _last_control_mode = None
    _user_args = None
    _joint_record = []
    _speed_record = []

    def __init__(self, config):
        self._config = config

    def user_command(self, control_mode, *args):
        self._last_control_mode = self._control_mode
        self._control_mode = control_mode
        self._user_args = args

    def update_duties(self, joints):
        geometry = Geometry(self._config.section_lengths, joints)
        speed = self._control_mode(self._config, joints, geometry, *self._user_args)
        # self.log(joints, geometry, speed)
        return speed

    #def log(self, joints, geometry, speed):
     #   timestamp = time.time()
      #  if self._last_control_mode != self._control_mode:
            # make a new record if the control mode changes
       #     self._speed_record.append([])
        # record state
        #self._speed_record[-1].append((*speed, self._control_mode.__class__.__name__, *self._user_args))
        #self._joint_record.append((*joints, *geometry.position, *geometry.dr, *geometry.dz))
