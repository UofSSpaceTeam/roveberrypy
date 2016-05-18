#ifndef ARM2016_FEEDBACK
#define ARM2016_FEEDBACK

#define ANALOG_READ_NSAMPLES 11
static int analog_read_samples[ANALOG_READ_NSAMPLES];

#define SMOOTH_DIFF_SIZE POSITION_LOG_DEPTH
static const double leading_coeff = 1.0/(8.0 * ((double)PERIOD_FEEDBACK_TASK/1000));
static const double term_coeffs[SMOOTH_DIFF_SIZE] = { 1.0, 2.0, -2.0, -1.0 };


int readPosition(int id);
int median(int arset[], int n);
double calculateVelocity(int id);

void updateFeedback() {
	// update g_position pointer
	--g_position;
	if (g_position < g_position_log) {
		g_position = g_position_log + POSITION_LOG_DEPTH - 1;
	}
	// update the g_position and velocity of each of the motors
	for(int i = 0; i < NUM_MOCS; ++i) {
		if(PINS_AI[i]) { // if we have feedback for this motor
			// Read g_position
			(*g_position)[i] = readPosition(i);
			// Calculate velocity
			g_velocity[i] = calculateVelocity(i);
		}
	}
}


int readPosition(int motor_id) {
	for(int i = 0; i < ANALOG_READ_NSAMPLES; ++i){
		analog_read_samples[i] = analogRead(PINS_AI[motor_id]);
	}
	return median(analog_read_samples, ANALOG_READ_NSAMPLES);
}

double calculateVelocity(int id) {
	int pos_idx = (g_position - g_position_log);
	int log_idx;
	double velo = 0;
	for(int d = 0; d < POSITION_LOG_DEPTH; ++d) {
		log_idx = (pos_idx + d) % POSITION_LOG_DEPTH;
		velo += term_coeffs[d] * g_position_log[log_idx][id];
	}
	return leading_coeff * velo;
}


int median(int arset[], int n)
{
	int i, j, l, m, x, t, k;
	k = n / 2;
	l = 0; m = n - 1;
	while (l<m) {
		x = arset[k];
		i = l;
		j = m;
		do {
			while (arset[i]<x) i++;
			while (x<arset[j]) j--;
			if (i <= j) {
				t = arset[i];
				arset[i] = arset[j];
				arset[j] = t;
				i++;
				j--;
			}
		} while (i <= j);
		if (j<k) l = i;
		if (k<i) m = j;
	}
	return arset[k];
}

#endif
