from math import *
import numpy as np
#import matplotlib.pyplot as plt

'''
Formulas taken from this paper:
http://www8.cs.umu.se/~thomash/reports/KinematicsEquationsForDifferentialDriveAndArticulatedSteeringUMINF-11.19.pdf
'''



def diff_drive_fk(x, y, l, theta, vl, vr, delta_t):
    """ Calculates forwark kinematics based on starting position,
        starting angle, width between wheels, velocity of wheels,
        and delta time.
        Returns: [x', y', theta']
    """
    if vr == vl:
        x_p = x + vr*cos(theta)*delta_t
        y_p = y + vr*sin(theta)*delta_t
        final = [x_p, y_p, theta]
    elif vr == -vl:
        omega = (vr-vl)/l
        theta_p = omega*delta_t + theta
        final = [x, y, theta_p]
    else:
        R = l/2*(vl + vr)/(vr-vl)
        omega = (vr-vl)/l

        ICC = (x-R*sin(theta), y+R*cos(theta))
        #theta = omega*delta_t + theta
        a = np.matrix([[cos(omega*delta_t), -sin(omega*delta_t), 0],
            [sin(omega*delta_t), cos(omega*delta_t), 0],
            [0, 0, 1]])
        b = np.matrix([[x-ICC[0]], [y-ICC[1]], [theta]])
        c = np.matrix([[ICC[0]], [ICC[1]], [omega*delta_t]])
        result = (np.matmul(a,b) + c).tolist()
        final = [result[0][0], result[1][0], result[2][0]]
    return final

def inverse_kinematics_drive(x,y,x_dst,y_dst,theta, l):
    """
        input:
            x,y: the starting position
            x_dst, y_dst: the destination position
            theta: the starting angle
            l: width between wheels
        output:
            ratio = vr / vl: the ratio of velocity of the two wheels
    """
    
    reverse = False
   
    
    if x_dst == x:
        if y_dst > y:
            gama = pi / 2
        else:
            gama = 3 * pi / 2
    else:
        gama = atan((y_dst - y)/(x_dst - x))
	
    if x_dst < x:
        gama = gama + pi
    
    omega = 2*(gama - theta)
    if omega == 0:
        return 1,False
    elif omega == 2 * pi:
        return 1, True
    elif omega > pi or omega < -1 * pi:
        omega = 2*pi - omega
        reverse = True
	
    d = sqrt((x_dst - x)**2 + (y_dst - y)**2)

    k = d / (l * sin(omega / 2))
    ratio = (k+1)/(k-1)

    return ratio,reverse

def differential_drive_test():

	print("---------------------------")
	print("Demoing Forward kinematics:")
	print("Starting point {}".format([0,0,np.pi/2]))

	print("drive straigt {}".format(
		diff_drive_fk(0,0,4,np.pi/2, np.pi, np.pi, 1)))
	print("drive straigt backwards{}".format(
		diff_drive_fk(0,0,4,np.pi/2, -np.pi, -np.pi, 1)))
	print("pivot left on left wheel {}".format(
		diff_drive_fk(0,0,4,np.pi/2, 0, np.pi, 1)))

	print("pivot right on right wheel {}".format(
		diff_drive_fk(0,0,4,np.pi/2, np.pi, 0, 1)))

	print("Rotate right (clockwise) {}".format(
		diff_drive_fk(0,0,4,np.pi/2, np.pi, -np.pi, 1)))

	print("Rotate left (counterclockwise) {}".format(
		diff_drive_fk(0,0,4,np.pi/2, -np.pi, np.pi, 1)))

	print("Curve to the left {}".format(
		diff_drive_fk(0,0,4,np.pi/2, np.pi, 1.1*np.pi, 1)))

	print("Curve to the right {}".format(
		diff_drive_fk(0,0,4,np.pi/2, 1.1*np.pi, np.pi, 1)))

	print("--------------------------")

def inverse_kinematics_test():
	x = 0
	y = 0
	theta = pi/3
	x_dst = 0
	y_dst = -15
	l = 1
	speed = 1
	plt.plot([x,x_dst], [y,y_dst])
	
	ratio,reverse = inverse_kinematics_drive(x,y,x_dst,y_dst,theta,l)
	print(ratio)
	if reverse:
		speed = -1
	trace_x = []
	trace_y = []
	x_tmp = x
	y_tmp = y
	theta_tmp = theta
	for i in range(30):
		[x_tmp,y_tmp,theta_tmp] = diff_drive_fk(x_tmp,y_tmp, l,theta_tmp, speed, ratio * speed, 1)
		trace_x.append(x_tmp)
		trace_y.append(y_tmp)
	plt.plot(trace_x,trace_y,'ro')
	plt.show()

if __name__ == "__main__":
	#differential_drive_test()
	inverse_kinematics_test()
