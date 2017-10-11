import unittest
import math
import random

class LimitTest(unittest.TestCase):
    def test(self):
        from arm import Limits
        limits = (
            Limits(-0.2, 0.2),
            Limits(-0.5, 0.5),
            None,
            Limits(-0.9, 0.2),
            Limits(-0.2, 0.9),
            None
        )
        p_duty = (1, 1, 1, 1, 1, 1)
        n_duty = (-1, -1, -1, -1, -1, -1)
        p_duty_ok_pos = (-0.3, -0.6, 100, -0.91, -0.21, 100)
        n_duty_ok_pos = (0.3, 0.6, -100, 0.9, 0.91, -100)
        self.assertEqual(Limits.enforce(limits, (p_duty_ok_pos), p_duty), (p_duty))
        self.assertEqual(Limits.enforce(limits, (n_duty_ok_pos), n_duty), (n_duty))
        self.assertEqual(Limits.enforce(limits, (p_duty_ok_pos), n_duty), (0, 0, -1, 0, 0, -1))
        self.assertEqual(Limits.enforce(limits, (n_duty_ok_pos), p_duty), (0, 0, 1, 0, 0, 1))
        misc_pos = (-0.19, 0.6, 100, -0.1, 0.1, 100)
        self.assertEqual(Limits.enforce(limits, (misc_pos), n_duty), (-1, -1, -1, -1, -1, -1))
        self.assertEqual(Limits.enforce(limits, (misc_pos), p_duty), (1, 0, 1, 1, 1, 1))


class GeometryTest(unittest.TestCase):

    def get_r_z(self, phi0, phi1):
        return math.sin(phi0) + math.sin(phi0 + phi1), math.cos(phi0) + math.cos(phi0 + phi1)

    def test(self):
        from arm import Geometry, Sections, Joints, CylindricalCoordinate
        lengths = Sections(1.0, 0.9, 0.1)
        for t in range(15):
            base = random.random()
            phi0 = random.random() / 1.5
            phi1 = random.random() / 1.5
            phi2 = 2 * (random.random() - 0.5)
            joints = Joints(base, phi0, phi1, phi2, None, None)
            geo = Geometry(lengths, joints)
            # check that postition is correct
            r, z = self.get_r_z(phi0, phi1)
            pos = CylindricalCoordinate(r, base, z)
            self.assertAlmostEqual(pos.r, geo.position.r)
            self.assertAlmostEqual(pos.theta, geo.position.theta)
            self.assertAlmostEqual(pos.z, geo.position.z)
            # check that hold values are correct
            dphi0, dphi1 = geo.hold_altitude()
            dz = dphi0 * geo.dz[0] + dphi1 * geo.dz[1]
            self.assertAlmostEqual(dz, 0.0)
            delta = 0.0175 # 5 deg/s for 0.2 s
            joints2 = Joints(
                base,
                phi0 + dphi0 * delta,
                phi1 + dphi1 * delta,
                phi2 + geo.maintain_wrist_pitch(dphi0 * delta, dphi1 *delta),
                None,
                None
            )
            geo2 = Geometry(lengths, joints2)
            tol = 0.001 # 1mm tol
            diff = geo2.position.z - geo.position.z
            self.assertTrue(diff < tol)

            dphi0, dphi1 = geo.hold_radius()
            dr = dphi0 * geo.dr[0] + dphi1 * geo.dr[1]
            self.assertAlmostEqual(dr, 0.0)
            delta = 0.0175  # 5 deg/s for 0.2 s
            joints2 = Joints(
                base,
                phi0 + dphi0 * delta,
                phi1 + dphi1 * delta,
                phi2 + delta * (dphi0 + dphi1),
                None,
                None
            )
            geo2 = Geometry(lengths, joints2)
            tol = 0.001  # 1mm tol
            diff = geo2.position.r - geo.position.r
            self.assertTrue(diff < tol)


class ManualControlTest(unittest.TestCase):

    def step_time(self, joints, duty, dt):
        from arm import Joints
        new_joints = list(joints)
        for i in range(len(duty)):
            if new_joints[i] is None:
                new_joints[i] = None
            else:
                new_joints[i] = joints[i] + duty[i] * dt
        return Joints(*tuple(new_joints))

    def test(self):
        from arm import Joints, Controller, ManualControl, Config
        joints = Joints(
            0,
            0.5,
            0.6,
            0.1,
            None,
            None
        )

        config = Config()
        controller = Controller(config)

        cmd = Joints(
            -1,
            -1,
            -1,
            -1,
            -1,
            -1
        )

        controller.user_command(ManualControl(), *cmd)

        # go until we're at the lower bound for each
        all_lower_bound = False
        while not all_lower_bound:
            duty = controller.update_duties(joints)
            all_zero = True
            for i in range(len(joints)):
                if not (joints[i] is None):
                    all_zero &= duty[i] == 0
                if duty[i] != 0:
                    self.assertAlmostEqual(duty[i], -config.max_angular_velocity[i])
            all_lower_bound = all_zero
            joints = self.step_time(joints, duty, 0.1)

        # go until we're at the upper bounds for each
        cmd = Joints(
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5
        )
        controller.user_command(ManualControl(), *cmd)
        all_upper_bound = False
        while not all_upper_bound:
            duty = controller.update_duties(joints)
            all_zero = True
            for i in range(len(joints)):
                if not (joints[i] is None):
                    all_zero &= duty[i] == 0
                if duty[i] != 0:
                    self.assertAlmostEqual(duty[i], 0.5 * config.max_angular_velocity[i])
            all_upper_bound = all_zero
            joints = self.step_time(joints, duty, 0.1)

        # move joints back a bit
        cmd = Joints(
            -1,
            -1,
            -1,
            -1,
            -1,
            -1
        )
        controller.user_command(ManualControl(), *cmd)
        duty = controller.update_duties(joints)
        for d in duty:
            self.assertAlmostEqual(d, -1 * config.max_angular_velocity[i])

        joints = self.step_time(joints, duty, 0.3)
        # turn them all off
        cmd = Joints(
            0,
            0,
            0,
            0,
            0,
            0
        )
        controller.user_command(ManualControl(), *cmd)
        duty = controller.update_duties(joints)
        for d in duty:
            self.assertAlmostEqual(d, 0)

class PlanarControlTest(unittest.TestCase):

    def step_time(self, joints, duty, dt):
        from arm import Joints
        new_joints = list(joints)
        for i in range(len(duty)):
            if new_joints[i] is None:
                new_joints[i] = None
            else:
                new_joints[i] = joints[i] + duty[i] * dt
        return Joints(*tuple(new_joints))

    def test(self):
        # dr, dz, base, wrist_pitch, wrist_roll, gripper
        from arm import Joints, Controller, PlanarControl, Config, Geometry
        joints = Joints(
            0,
            0.5,
            0.6,
            0.1,
            None,
            None
        )

        start_wrist_pitch = joints.shoulder + joints.elbow + joints.wrist_pitch

        config = Config()
        controller = Controller(config)
        start_pos = Geometry(config.section_lengths, joints)
        cmd = (
            -1,  # decrease radius
            0,
            -1,
            0,
            -1,
            -1
        )

        controller.user_command(PlanarControl(), *cmd)

        # go until we're at the lower bound for each
        all_lower_bound = False
        while not all_lower_bound:
            duty = controller.update_duties(joints)
            all_zero = True
            for i in range(len(joints)):
                if not (joints[i] is None):
                    all_zero &= duty[i] == 0
            for j in [0, 4, 5]:
                if duty[j] != 0:
                    self.assertAlmostEqual(duty[j], -config.max_angular_velocity[j])
            joints = self.step_time(joints, duty, 0.05)
            all_lower_bound = all_zero
        end_pos = Geometry(config.section_lengths, joints)

        dr = start_pos.position.r - end_pos.position.r
        dz = start_pos.position.z - end_pos.position.z

        diff = abs(dz/dr)
        self.assertTrue(diff < 0.02)










if __name__ == "__main__":
    unittest.main()








