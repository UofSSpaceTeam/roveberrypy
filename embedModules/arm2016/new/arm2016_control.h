#ifndef ARM2016_CONTROL
#define ARM2016_CONTROL

#include "arm2016_vars.h"
#include "arm2016_dcm.h"

void updateControllers() {
	// update the duty-cycle's
	if(g_ramping_enabled) {
		DCManager_update();
    DCManager_correct(3);
    DCManager_correct(4);
	}
	// update motor controllers
	for(int i = 0; i < NUM_MOCS; ++i) {
		// set direction
		if(g_duty_cycle[i] * DIR_CORRECTION[i] >= 0) {
			// motor should go forwards
			digitalWrite(PINS_A[i], HIGH);
			digitalWrite(PINS_B[i], LOW);
			if (PINS_PWM[i]) {	// check if the pin exists
				analogWrite(PINS_PWM[i], g_duty_cycle[i]);
			}
		} else {
			// motor should go backwards
			digitalWrite(PINS_A[i], LOW);
			digitalWrite(PINS_B[i], HIGH);
			if (PINS_PWM[i]) {	// check if the pin exists
				analogWrite(PINS_PWM[i], -g_duty_cycle[i]);
			}
		}
	}
}

#endif
