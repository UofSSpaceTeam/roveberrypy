#ifndef POSITION_CONSTRAINT_H
#define POSITION_CONSTRAINT_H

/**
 *  Used to set to position constraints on a linear actuator.
 *  @author Liam Bindle
 *  \ingroup types
 */
struct PositionConstraint{
	float max; /**< The maximum allowable position. Unit: [mm] */
	float min; /**< The minimum allowable position. Unit: [mm] */
};


#endif
