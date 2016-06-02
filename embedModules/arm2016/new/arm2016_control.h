#ifndef ARM2016_CONTROL
#define ARM2016_CONTROL

#include "arm2016_vars.h"
#include "arm2016_dcm.h"

void updateControllers() {
	// update the duty-cycle's
	if(g_ramping_enabled) {
		DCManager_update();
		if(!g_ivk_controller) {
		    DCManager_correct(3);
		    DCManager_correct(4);
		}
	}
	// update motor controllers
	Serial.print("setting motors");
	for(int i = 0; i < NUM_MOCS; ++i) {
		// set direction
		Serial.print(g_duty_cycle[i]);
		Serial.print(",");
		if(g_duty_cycle[i] * DIR_CORRECTION[i] >= 0) {
			// motor should go forwards
			if (PINS_PWM[i]) {	// check if the pin exists
				digitalWrite(PINS_A[i], HIGH);
				digitalWrite(PINS_B[i], LOW);
				analogWrite(PINS_PWM[i], g_duty_cycle[i]);
			} else {
				if(g_duty_cycle[i] == 0){
					digitalWrite(PINS_A[i], LOW);
					digitalWrite(PINS_B[i], LOW);
				} else {
					digitalWrite(PINS_A[i], HIGH);
					digitalWrite(PINS_B[i], LOW);
				}
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
	Serial.println();
}

#endif
