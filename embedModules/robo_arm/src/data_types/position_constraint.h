#ifndef POSITION_CONSTRAINT_H
#define POSITION_CONSTRAINT_H

/**
 *  @file position_constraint.h
 */

/**
 *  Used to set to position constraints on a linear actuator.
 *  @author Liam Bindle
 *  \ingroup posConstraint
 */
typedef struct PositionConstraint {
	const float MAX; /**< The maximum allowable position. Unit: [mm] */
	const float MIN; /**< The minimum allowable position. Unit: [mm] */
} PositionConstraint;

/**
 *  Instantiate a position constraint.
 *  @author Liam Bindle
 *  @param MIN The minimum constraint.
 *  @param MAX The maximum constraint.
 *  @return A pointer to the new PositionConstraint instance.
 *  \ingroup posConstraint
 */
PositionConstraint* new_PositionConstraint(const float MIN, const float MAX);

#endif
