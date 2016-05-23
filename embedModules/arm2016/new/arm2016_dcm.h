#ifndef ARM2016_DCM
#define ARM2016_DCM

#include "arm2016_vars.h"

void DCManager_init(int motor_idx);

void smartMove(int motor, int position)
{
    g_ramping_enabled = true;
    g_destination[motor] = position;
    DCM_corrections[motor] = 0;
    DCManager_init(motor);
}

void DCManager_correct(int motor_id) {
  if(DCM_stages[motor_id] == DONE && DCM_corrections[motor_id] < DCM_max_corrections[motor_id]) {
    DCM_corrections[motor_id] = DCM_corrections[motor_id] + 1;
    g_elapsed_cycles[motor_id] = 0;
    DCM_stages[motor_id] = RAMP_UP;
  }
}

void DCManager_init(int motor_idx)
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
    DCM_stages[0] = DONE;
    DCM_stages[1] = DONE;
    if(motor_idx == 2 && DCM_stages[2] == DONE) {
      DCM_stages[2] = RAMP_UP;
      g_elapsed_cycles[2] = 0;
    }
    if(motor_idx == 3 && DCM_stages[3] == DONE) {
      DCM_stages[3] = RAMP_UP;
      g_elapsed_cycles[3] = 0;
    }
    if(motor_idx == 4 && DCM_stages[4] == DONE) {
      DCM_stages[4] = RAMP_UP;
      g_elapsed_cycles[4] = 0;
    }
    if(motor_idx == 5 && DCM_stages[5] == DONE){
      DCM_stages[5] = RAMP_UP;
      g_elapsed_cycles[5] = 0;
    }
}

// Update the duty-cycle for each movement.
// @param elapsed_ms Elapsed time in milliseconds since movements began.
void DCManager_update()
{
	// Find the max distance remaining

    int* dc = g_duty_cycle;
	double max_dist = 0;
	for (uint_t i = 2; i < DCM_SIZE; ++i) {
        if(DCM_stages[i] != DONE) {
            DCM_dists[i] = g_destination[i] - (*g_position)[i];
            DCM_vels[i] = abs(g_velocity[i]);
    		if (abs(DCM_dists[i]) > max_dist) max_dist = abs(DCM_dists[i]);
        }
	}
	// Loop through each movement
	for (uint_t i = 2; i < DCM_SIZE; ++i) {
        ++g_elapsed_cycles[i];         // increment the number of elapsed cycles
        double elapsed_ms = g_elapsed_cycles[i] * DCM_PERIOD_MS;
		// Check if the movement has finished and that we're moving in the right direction
    if (DCM_stages[i] != DONE && abs(DCM_dists[i]) < DCM_tolerance[i]) {
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
			} else {
        // check if we're going in the right direction. if we aren't then say we're done
        if(DCM_dists[i] > 0 && dc[i] < 0) {
          DCM_stages[i] = DONE;
        } else if (DCM_dists[i] < 0 && dc[i] > 0) {
          DCM_stages[i] = DONE;
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
