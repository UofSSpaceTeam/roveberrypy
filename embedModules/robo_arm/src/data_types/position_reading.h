#ifndef POSITION_READING_H
#define POSITION_READING_H

/**
 *  @file position_reading.h
 */

/**
 *  Used to organize position readings. Contains the position at a given time.
 *  Note that there is a time_fine and time_base. The actual time would be 
 *  given by time_fine + time_base but they have been broken up here to avoid
 *  numeric instabilities. Thus 0 < time_fine < 1000.
 *  @author Liam Bindle
 *  \ingroup posReading
 */
typedef struct PositionReading{
	const float POSITION; /**< The position of the linear actuator. Unit: [mm] */
	const int TIME_MS;	/**< The time of the reading. Unit: [ms] */
	const int TIME_S;	/**< The time of the reading. Unit: [s]  */
} PositionReading;

/**
 *  Instantiate a PositionReading instance.
 *  @param position The position of the reading. [mm]
 *  @param time The time of the reading. [s]
 *  @return Pointer to the instantiation. 
 *  @author Liam Bindle
 *  \ingroup posReading
 */
PositionReading *new_PositionReading(float position, float time);

/**
 *  Get the position from the reading.
 *  @param reading The instance to get the position from.
 *  @return The position in mm.
 *  @author Liam Bindle
 *  \ingroup posReading
 */
float getPosition(PositionReading* reading);

/**
 *  Get the time the reading was taken.
 *  @param reading The query instance.
 *  @return The time the reasing was taken
 *  @author Liam Bindle
 *  \ingroup posReading
 */
float getTime(PositionReading* reading);

/**
 *  The difference in time between two readings.
 *  @param newer_reading The most recent of the two readings.
 *  @param older_reading The older of the two readings.
 *  @return The difference in time between the readings. [seconds]
 *  @author Liam Bindle
 *  \ingroup posReading
 */
float getTimeDifference_s(PositionReading* newer_reading, PositionReading* older_reading);

/**
 *  The difference in time between two readings.
 *  @param newer_reading The most recent of the two readings.
 *  @param older_reading The older of the two readings.
 *  @return The difference in time between the readings. [milliseconds]
 *  @author Liam Bindle
 *  \ingroup posReading
 */
float getTimeDifference_ms(PositionReading* , PositionReading* );

/**
 *  The difference in position between two readings.
 *  @param newer_reading The most recent of the two readings.
 *  @param older_reading The older of the two readings.
 *  @return The difference in position between the two postions. [mm]
 *  @author Liam Bindle
 *  \ingroup posReading
 */
float getPositionDifference(PositionReading*, PositionReading*);



#endif
