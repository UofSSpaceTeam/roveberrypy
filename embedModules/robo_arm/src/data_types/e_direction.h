#ifndef E_DIRECTION_H
#define E_DIRECTION_H

/**
 *  @file e_direction.h
 */

/**
 * @enum e_MOTOR_DIRECTION
 * \ingroup dirEnum
 * Used to specify the direction of a motor.
 * @author Liam Bindle
 */
typedef enum e_MOTOR_DIRECTION	
{
	CCW, /**< Counterclockwise rotation. */
	CW	/**< Counterclockwise rotation. */

} e_MOTOR_DIRECTION;



/**
 * @enum e_LA_DIRECTION
 * \ingroup dirEnum
 * Used to specify the direction a linear actuator is moving.
 * @author Liam Bindle
 */
typedef enum e_LA_DIRECTION
{
	EXTEND, /**< The actuator is extending. */
	RETRACT	/**< The actuator is retracting. */
}e_LA_DIRECTION;


#endif
