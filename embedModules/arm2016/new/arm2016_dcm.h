#ifndef ARM2016_DCM
#define ARM2016_DCM

#include "arm2016_vars.h"

void DCManager_init()
{
#ifdef DCM_DEBUG
    Serial.println("Initializing duty-cycle manager");
    Serial.print("Ramp-up time (ms):");
    Serial.println(TIME_RAMP_UP_MS);
    Serial.print("DCM period (ms):");
    Serial.println(DCM_PERIOD_MS);
    Serial.print("DCM_MIN_VEL_INC=");
    Serial.println(DCM_MIN_VEL_INC);
#endif
    for (uint_t i = 3; i < DCM_SIZE; ++i) {
        DCM_stages[i] = RAMP_UP;
    }
}

// Update the duty-cycle for each movement.
// @param elapsed_ms Elapsed time in milliseconds since movements began.
void DCManager_update()
{
	// Find the max distance remaining
    double elapsed_ms = g_elapsed_cycles * DCM_PERIOD_MS;
    int* dc = g_duty_cycle;
    DCM_dists[3] = g_destination[3] - (*g_position)[3];
	DCM_vels[3] = abs(g_velocity[3]);
	double max_dist = abs(DCM_dists[3]);
	for (uint_t i = 4; i < DCM_SIZE; ++i) {
        DCM_dists[i] = g_destination[i] - (*g_position)[i];
        DCM_vels[i] = abs(g_velocity[i]);
		if (abs(DCM_dists[i]) > max_dist) max_dist = abs(DCM_dists[i]);
	}
	// Loop through each movement
	for (uint_t i = 3; i < DCM_SIZE; ++i) {                                        // ONLY USE DCM FOR MOTORS WITH FEEDBACK
		// Check if the movement has finished
		if (DCM_stages[i] != DONE && (abs(DCM_dists[i]) < DCM_tolerance[i])) {
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
			else if (abs(DCM_dists[i]) < DCM_rd_dists[i]) {
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
			if (abs(DCM_dists[i]) < DCM_rd_dists[i]) {
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
			if (DCM_vels[i] <= MIN_VEL_TOL * DCM_min_vels[i]) { // If we're close to the minimum velocity then increment stage
				DCM_stages[i] = MIN_VEL;
			}
			else {
				dc[i] = (int) (scale * abs(DCM_dists[i]) / DCM_rd_dists[i]);
			}
			break;
		}
		break;
		// Once near the minimum velocity, hold it until we reach the destination
		case MIN_VEL:
		{
			int abs_dc = abs(dc[i]);
			if (DCM_vels[i] < DCM_min_vels[i]) {
                if(DCM_dists[i] > 0){
                     dc[i] = (int) (abs_dc + DCM_MIN_VEL_INC * (DCM_min_vels[i] - DCM_vels[i]) / DCM_min_vels[i]);
                 } else {
                     dc[i] = (int) -(abs_dc + DCM_MIN_VEL_INC * (DCM_min_vels[i] - DCM_vels[i]) / DCM_min_vels[i]);
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

#ifdef DCM_DEBUG
        Serial.print(i);
        Serial.print(": dist=");
        Serial.print(DCM_dists[i]);
        Serial.print(", vels=");
        Serial.print(DCM_vels);
        Serial.print(", dc=");
        Serial.print(dc[i]);
        Serial.print(", stage=");
        switch (DCM_stages[i]) {
        case RAMP_UP:
            Serial.print("RAMP_UP");
            break;
        case POSITION_SYNC:
            Serial.print("POSITION_SYNC")
            break;
        case RAMP_DOWN:
            Serial.print("RAMP_DOWN")
            break;
        case MIN_VEL:
            Serial.print("MIN_VEL");
            break;
        }
        Serial.println("");
#endif
	}
}
#endif
