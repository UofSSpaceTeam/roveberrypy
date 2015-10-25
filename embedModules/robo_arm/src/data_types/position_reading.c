#include "position_reading.h"
#include <stdlib.h>


PositionReading *new_PositionReading(float position, float time){
	PositionReading *temp = malloc(sizeof(PositionReading));
	/* Set position */
	*(float *)&temp->POSITION = position;
	
	/* Seconds */
	*(int *)&temp->TIME_S = (int)time; 
	
	/* Milliseconds */
	*(int *)&temp->TIME_MS = (int)((time - temp->TIME_S)*1000);
	
	return temp;
}

float getPosition(PositionReading* reading){
	return reading->POSITION;
}

float getTime(PositionReading* readingInstance){
	return (float)(readingInstance->TIME_S) + (float)(readingInstance->TIME_MS)/1000.0;
}

float getTimeDifference_s(PositionReading* newerReading, PositionReading* olderReading){
	int seconds = newerReading->TIME_S - olderReading->TIME_S;
	float milliseconds = (float)(newerReading->TIME_MS - olderReading->TIME_MS)/1000.0;
	return seconds + milliseconds;
}

float getPositionDifference(PositionReading* newerReading, PositionReading* olderReading){
	return newerReading->POSITION - olderReading->POSITION;
}

float getTimeDifference_ms(PositionReading* newerReading, PositionReading* olderReading){
	if(newerReading->TIME_S == olderReading->TIME_S){
		return newerReading->TIME_MS - olderReading->TIME_MS;
	} else {
		float sec = (newerReading->TIME_S-olderReading->TIME_S);
		return (newerReading->TIME_MS + sec*1000) - olderReading->TIME_MS;
	}
	
}