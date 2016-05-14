#ifndef ARM2016_VARS
#define ARM2016_VARS

#define POSITION_LOG_DEPTH 16
#define NUM_MOCS 6

int 		destination		[NUM_MOCS];
int 		position		[NUM_MOCS];
int 		position_log	[POSITION_LOG_DEPTH]	[NUM_MOCS];
double		velocity		[NUM_MOCS];
int			duty_cycle		[NUM_MOCS];

bool		ramping_enabled;
int			elapsed_cycles;

#endif
