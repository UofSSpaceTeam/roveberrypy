

#include "arm2016_vars.h"

static		double		norm_dists		[NUM_MOCS];

void controlTask() {
	// update the duty-cycle's
	if(ramping_enabled) {
		DCManager_update(elapsed_cycles * cntrl_tsk_period, position, velocity, duty_cycle)
	}
	
	for(int i = 0; i < NUM_MOCS; ++i) {
		// set direction
		if(duty_cycle[i] > 0) {		// motor should go forwards
			// ...
		} else {					// motor should go backwards
			// ...
		}
		
		// set the duty-cycle
		// ...
	}

}
