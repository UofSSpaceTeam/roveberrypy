#ifndef VNH3SP30_H
#define VNH3SP30_h

typedef struct{
	const unsigned int A;
	const unsigned int B;
	const unsigned int PWM;
} vnh3sp30;

/**
 *  Initialize an VNH3SP30 controller.
 *  @param A Pinout for A
 *  @param B Pinout for B
 *  @param PWM Pinout for PWM
 */
void init_VNH3SP30(unsigned int A, unsigned int B, unsigned int PWM);

/**
 *  Initialize an VNH3SP30 controller.
 *  @param A Pinout for A
 *  @param B Pinout for B
 */
void init_VNH3SP30(unsigned int A, unsigned int B);

/**
 *  Used to control an instance of VNH3SP30 used for an actuator.
 *  @param mc The motor controller of interest.
 *  @param dir The direction of the actuator
 *  @param pwm The duty cycle to be sent to the motor contoller
 */
int setVNH3SP30(vnh3sp30 mc, e_LA_DIRECTION dir, unsigned int pwm);

/**
 *  Used to control an instance of VNH3SP30 used for a motor.
 *  @param mc The motor controller of interest.
 *  @param dir The direction of the motor
 *  @param pwm The duty cycle to be sent to the motor contoller
 */
int setVNH3SP30(vnh3sp30 mc, e_MOTOR_DIRECTION dir, unsigned int pwm);

/**
 *  Used to imediately stop whatever motor or actuator mc is.
 *  @param mc the motor controller to be stopped.
 */
int stopVNH3SP30(vnh3sp30 mc);


#endif
