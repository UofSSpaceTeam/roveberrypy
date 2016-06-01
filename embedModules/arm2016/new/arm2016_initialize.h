#ifndef ARM2016_INIT
#define ARM2016_INIT

#include "arm2016_vars.h"
#include <Wire.h>
#include "arm2016_comms.h" // for Wire.onReceive
#include "arm2016_feedback.h"

#define     INITIAL_RADIUS      0.4
#define     INITIAL_ALTITUDE    0.3

void arm2016_init()
{
    // set pin mode
    for(uint_t i = 0; i < NUM_MOCS; ++i) {
        pinMode(PINS_A[i], OUTPUT);
        pinMode(PINS_B[i], OUTPUT);
    }
    // flush feedback
    for(uint_t i = 0; i < POSITION_LOG_DEPTH; ++i) {
        updateFeedback();
    }
    // initialize all variables
    for(uint_t i = 0; i < NUM_MOCS; ++i) {
        g_destination[i] = (*g_position)[i];
        g_duty_cycle[i] = 0;
        g_velocity[i] = 0;
        DCM_stages[i] = DONE;
    }
	 pinMode(BASE_INT, INPUT_PULLUP);
	 Wire.begin(I2C_ADDRESS);
	 Wire.onReceive(receiveCommand);
	 Wire.onRequest(sendPosition);
	 attachInterrupt(BASE_INT, baseCounterInterupt, CHANGE);

     // move to initial position
    //  double r0 = INITIAL_RADIUS;
    //  double z0 = INITIAL_ALTITUDE;
    //  CalculatePositions(r0, z0);
    //  g_ramping_enabled = true;
    //  DCM_corrections[3] = 0;
    //  DCManager_init(3);
    //  DCM_corrections[4] = 0;
    //  DCManager_init(4);
}


#endif
