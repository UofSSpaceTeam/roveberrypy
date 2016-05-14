#ifndef ARM2016_FEEDBACK
#define ARM2016_FEEDBACK

int readPosition(int id);

void updateFeedback() {
	
	// update position pointer
	position -= NUM_MOCS;
	if(position < position_log) {
		position = position_log + LOG_SIZE - NUM_MOCS;
	}
	
	// update the position and velocity of each of the motors
	for(int i = 0; i < NUM_MOCS; ++i) {
		// Read position
		position[i] = readPosition(i);
		
		// Calculate velocity
		velocity[i] = calculateVelocity(i);
	}
}


int readPosition(int id) {
	int ar = analogRead(PINS_AI[i]);
	return velo;
}

double calculateVelocity(int id) {
	int pos_idx = (position - position_log)/NUM_MOCS;
	int log_idx;
	double velo = 0;
	for(int d = 0; d < POSITION_LOG_DEPTH; ++d) {
		log_idx = (pos_idx + d) % POSITION_LOG_DEPTH;
		// position of motor i at depth=`d` is position_log[log_idx][i]
		velo += position[log_idx][i] ...
	}
	return velo;
}

#endif