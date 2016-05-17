#ifndef ARM2016_DCM
#define ARM2016_DCM
#include "arm2016_vars.h"

typedef unsigned int uint_t;

// Enumeration of Ramp-Function Stages
typedef enum {
	RAMP_UP,
	POSITION_SYNC,
	RAMP_DOWN,
	MIN_VEL,
	DONE
} ERFStage;

// Basic configuration
#define DCM_SIZE 6
#define MAX_DC 255.0

// Duty-cycle manager variables
static const    double  TIME_RAMP_UP_MS = 300;     //  Time of ramp-up
static const    double  DCM_PERIOD_MS = 100;      //  Period of duty-cycle manager
static const    double  DCM_MIN_VEL_INC = MAX_DC * DCM_PERIOD_MS / TIME_RAMP_UP_MS;
static const    double  DCM_rd_dists[DCM_SIZE] = {  // ramp-down distances of movements
    50, 50, 50, 50, 50, 50
};
static const    double  DCM_min_vels[DCM_SIZE] = {  // minimum velocities for MIN_VELO stage of movements
    10, 10, 10, 10, 10, 10
};
static const    double  DCM_tolerance[DCM_SIZE] = {
    5, 5, 5, 5, 5, 5
}
static          double  DCM_dists[DCM_SIZE];
static          double  DCM_vels[DCM_SIZE];
static          ERFStage DCM_stages[DCM_SIZE];  // stages of movements

void DCManager_init()
{
#ifdef DCM_DEBUG
    Serial.println("Initializing duty-cycle manager");
    Serial.print("Ramp-up time:")
    Serial.print(TIME_RAMP_UP_MS);
#endif
    for (uint_t i = 0; i < DCM_SIZE; ++i) {
        DCM_stages[i] = RAMP_UP;
    }
}
// Update the duty-cycle for each movement.
// @param elapsed_ms Elapsed time in milliseconds since movements began.
void DCManager_update()
{
	// Find the max distance remaining
    double elapsed_ms = g_elapsed_cycles * DCM_PERIOD_MS / 1000;
    int* dc = g_duty_cycle;
    DCM_dists[0] = g_destination[0] - (*g_position)[0];
	double max_dist = abs(DCM_dists[0]);
	for (uint_t i = 1; i < DCM_SIZE; ++i) {
        DCM_dists[i] = g_destination[i] - (*g_position)[i];
        DCM_vels[i] = g_velocity[i];
		if (abs(DCM_dists[i]) > max_dist) max_dist = abs(DCM_dists[i]);
	}
	// Loop through each movement
	for (uint_t i = 0; i < DCM_SIZE; ++i) {
		// Check if the movement has finished
		if (DCM_stages[i] != DONE && (abs(DCM_dists[i]) < DCM_tolerance[i]) {
			DCM_stages[i] = DONE;
		}
		// Calculate the duty-cycle scale for this movement
		double scale = MAX_DC * DCM_dists[i] / max_dist;
		// Assign duty-cycle based on ramp-function stage
		switch (DCM_stages[i]) {
			// Ramp-up the duty-cycle for this movement
		case RAMP_UP:
		{
			double t = elapsed_ms / TIME_RAMP_UP_MS;
			if (elapsed_ms > TIME_RAMP_UP_MS) {
				DCM_stages[i] = POSITION_SYNC;
			}
			else if (DCM_dists[i] < DCM_rd_dists[i]) {
				DCM_stages[i] = RAMP_DOWN;
			}
			else {
				dc[i] = (int)(scale * t * t * (3.0 - 2.0 * t));
			}
		}
		break;
		// Syncronize the relative position of this movement with the others
		case POSITION_SYNC:
		{
			if (DCM_dists[i] < DCM_rd_dists[i]) {
				DCM_stages[i] = RAMP_DOWN;
			}
			else {
				dc[i] = (int)scale;
			}
		}
		break;
		// Ramp-down the duty-cycle until we're near the minimum velocity
		case RAMP_DOWN:
		{
			if (abs(DCM_vels[i]) <= 1.2 * DCM_min_vels[i]) { // If we're within 20% of the minimum velocity then increment stage
				DCM_stages[i] = MIN_VEL;
			}
			else {
				dc[i] = scale * abs(DCM_dists[i]) / DCM_rd_dists[i];
			}
			break;
		}
		break;
		// Once near the minimum velocity, hold it until we reach the destination
		case MIN_VEL:
		{
			if (abs(DCM_vels[i]) < DCM_min_vels[i]) {
                if(DCM_dists[i] > 0){
                     dc[i] = (int) (abs_dc[i] + DCM_MIN_VEL_INC * (DCM_min_vels[i] - abs(DCM_vels[i])) / DCM_min_vels[i]);
                 } else {
                     dc[i] = (int) -(abs_dc[i] + DCM_MIN_VEL_INC * (DCM_min_vels[i] - abs(DCM_vels[i])) / DCM_min_vels[i]);
                 }
			}
		}
		break;
		// If we're done then make sure the duty-cycle is 0
		case DONE:
		{
			dc[i] = 0;
		}
		break;
		};
	}
}

#endif
