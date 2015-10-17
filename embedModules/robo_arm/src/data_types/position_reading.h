#ifndef POSITION_READING_H
#define POSITION_READING_H

/**
 *  Used to organize position readings. Contains the position at a given time.
 *  Note that there is a time_fine and time_base. The actual time would be 
 *  given by time_fine + time_base but they have been broken up here to avoid
 *  numeric instabilities. Thus 0 < time_fine < 1000.
 *  @author Liam Bindle
 *  \ingroup types
 */
struct PositionReading{
	float position; /**< The position of the linear actuator. Unit: [mm] */
	int time_fine;	/**< The time of the reading. Unit: [ms] */
	int time_base;	/**< The time of the reading. Unit: [s]  */
};


#endif
