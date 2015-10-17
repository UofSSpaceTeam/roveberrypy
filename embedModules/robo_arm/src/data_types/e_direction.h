#ifndef E_DIRECTION_H
#define E_DIRECTION_H

/**
 *  @file e_direction.h
 */

/**
 * @enum e_MOTOR_DIRECTION
 * \ingroup types
 * Used to specify the direction of a motor.
 * @author Liam Bindle
 */
enum e_MOTOR_DIRECTION	
{
	CCW, /**< Counterclockwise rotation. */
	CW	/**< Counterclockwise rotation. */

};



/**
 * @enum e_LA_DIRECTION
 * \ingroup types
 * Used to specify the direction a linear actuator is moving.
 * @author Liam Bindle
 */
enum e_LA_DIRECTION
{
	EXTEND, /**< The actuator is extending. */
	RETRACT	/**< The actuator is retracting. */
};


#endif
