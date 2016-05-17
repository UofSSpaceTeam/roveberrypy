#ifndef ARM2016_CONTROL
#define ARM2016_CONTROL

#include "arm2016_vars.h"
#include "arm2016_dcm.h"


extern void digitalWrite(int, int);
extern void analogWrite(int, int);

#define HIGH 1
#define LOW 0

void updateControllers() {
	// update the duty-cycle's
	if(g_ramping_enabled) {
		++g_elapsed_cycles;
		DCManager_update();
	}
	// update motor controllers
	for(int i = 0; i < NUM_MOCS; ++i) {
		// set direction
		if(g_duty_cycle[i] >= 0) {
			// motor should go forwards
			digitalWrite(PINS_A[i], HIGH);
			digitalWrite(PINS_B[i], LOW);
			analogWrite(PINS_PWM[i], g_duty_cycle[i]);
		} else {
			// motor should go backwards
			digitalWrite(PINS_A[i], LOW);
			digitalWrite(PINS_B[i], HIGH);
			analogWrite(PINS_PWM[i], -g_duty_cycle[i]);
		}
	}
}

#endif
