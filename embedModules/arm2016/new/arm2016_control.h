#ifndef ARM2016_CONTROL
#define ARM2016_CONTROL

#include "arm2016_vars.h"

void updateControllers() {
	// update the duty-cycle's
	if(ramping_enabled) {
		DCManager_update(...)
	}
	
	// update motor controllers
	for(int i = 0; i < NUM_MOCS; ++i) {
		// set direction
		if(duty_cycle[i] >= 0) {	
			// motor should go forwards
			digitalWrite(PINS_A[i], HIGH);
			digitalWrite(PINS_B[i], LOW);
			analogWrite(PINS_PWM[i], duty_cycle[i]);
		} else {					
			// motor should go backwards
			digitalWrite(PINS_A[i], LOW);
			digitalWrite(PINS_B[i], HIGH);
			analogWrite(PINS_PWM[i], -duty_cycle[i]);
		}
	}
}

#endif