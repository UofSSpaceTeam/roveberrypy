#ifndef ARM2016_VARS
#define ARM2016_VARS

#include <limits.h>
#include "communications.cpp"

// Task period definitions
#define 		PERIOD_CONTROL_TASK		100
#define 		PERIOD_FEEDBACK_TASK	100
#define 		PERIOD_COMM_TASK		100

// Sizing definitions
#define 		POSITION_LOG_DEPTH 		16
#define 		NUM_MOCS 				6

// Global variables
int 			destination				[NUM_MOCS];
int 			position				[NUM_MOCS];
int 			position_log			[POSITION_LOG_DEPTH][NUM_MOCS];
double			velocity				[NUM_MOCS];
int				duty_cycle				[NUM_MOCS];
bool			ramping_enabled			= false;
int				elapsed_cycles			= 0;
packet			g_command			= NULL;

// Motor limits
const int		limits_min				[NUM_MOCS] = {
	INT_MIN,
	INT_MIN,
	INT_MIN,
	INT_MIN,
	INT_MIN,
	INT_MIN
};
const int 		limits_max				[NUM_MOCS] = {
	INT_MAX,
	INT_MAX,
	INT_MAX,
	INT_MAX,
	INT_MAX,
	INT_MAX
};

#endif
