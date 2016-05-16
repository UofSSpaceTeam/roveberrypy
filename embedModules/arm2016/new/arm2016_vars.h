#ifndef ARM2016_VARS
#define ARM2016_VARS

#include <limits.h>

// Task period definitions
#define 		PERIOD_CONTROL_TASK		100
#define 		PERIOD_FEEDBACK_TASK	100
#define 		PERIOD_COMM_TASK		100

// Sizing definitions
#define 		POSITION_LOG_DEPTH 		4
#define 		NUM_MOCS 				6
#define 		LOG_SIZE				POSITION_LOG_DEPTH*NUM_MOCS

// Global variables
int 			destination				[NUM_MOCS];
int				(*position)	[NUM_MOCS] 	= position_log;
int 			position_log			[POSITION_LOG_DEPTH][NUM_MOCS];
double			velocity				[NUM_MOCS];
int				duty_cycle				[NUM_MOCS];
bool			ramping_enabled			= false;
int				elapsed_cycles			= 0;
packet			g_command				= NULL;

// Pinout
const int		PINS_A					[NUM_MOCS] = {


};
const int		PINS_B					[NUM_MOCS] = {


};
const int		PINS_PWM				[NUM_MOCS] = {


};
const int		PINS_AI					[NUM_MOCS] = {

};

// Motor limits
const int		LIMITS_MIN				[NUM_MOCS] = {
	INT_MIN,
	INT_MIN,
	INT_MIN,
	INT_MIN,
	INT_MIN,
	INT_MIN
};
const int 		LIMITS_MAX				[NUM_MOCS] = {
	INT_MAX,
	INT_MAX,
	INT_MAX,
	INT_MAX,
	INT_MAX,
	INT_MAX
};

#endif
