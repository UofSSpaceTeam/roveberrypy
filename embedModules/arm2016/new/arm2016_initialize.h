#ifndef ARM2016_INIT
#define ARM2016_INIT

#include "arm2016_vars.h"
#include <Wire.h>
#include "arm2016_comms.h" // for Wire.onReceive

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
	 Wire.begin(I2C_ADDRESS);
	 Wire.onReceive(receiveCommand);
	 Wire.onRequest(sendPosition);

}


#endif
