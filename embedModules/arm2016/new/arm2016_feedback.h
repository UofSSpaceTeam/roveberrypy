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
	// update position pointer
	--position;
	if (position < position_log) {
		position = position_log + POSITION_LOG_DEPTH - 1;
	}
	// update the position and velocity of each of the motors
	for(int i = 0; i < NUM_MOCS; ++i) {
		// Read position
		(*position)[i] = readPosition(i);
		// Calculate velocity
		velocity[i] = calculateVelocity(i);
	}
}


int readPosition(int id) {
	for(int i = 0; i < ANALOG_READ_NSAMPLES; ++i){
		analog_read_samples[i] = analogRead(PINS_AI[i]);
	}
	return median(analog_read_samples, ANALOG_READ_NSAMPLES);
}

double calculateVelocity(int id) {
	int pos_idx = (position - position_log);
	int log_idx;
	double velo = 0;
	for(int d = 0; d < POSITION_LOG_DEPTH; ++d) {
		log_idx = (pos_idx + d) % POSITION_LOG_DEPTH;
		velo += term_coeffs[d] * position_log[log_idx][id];
	}
	return leading_coeff * velo;
}


int median(int arset[], int n)
{
	int i, j, l, m, x, t, k;
	k = n / 2;
	l = 0; m = n - 1;
	while (l<m) {
		x = a[k];
		i = l;
		j = m;
		do {
			while (a[i]<x) i++;
			while (x<a[j]) j--;
			if (i <= j) {
				t = a[i];
				a[i] = a[j];
				a[j] = t;
				i++;
				j--;
			}
		} while (i <= j);
		if (j<k) l = i;
		if (k<i) m = j;
	}
	return a[k];
}

#endif
