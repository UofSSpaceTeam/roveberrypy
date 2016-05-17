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
int 			g_destination			[NUM_MOCS];
int				(*g_position)			[NUM_MOCS] = position_log;
int 			g_position_log			[POSITION_LOG_DEPTH][NUM_MOCS];
double			g_velocity				[NUM_MOCS];
int				g_duty_cycle			[NUM_MOCS];
bool			g_ramping_enabled		= false;
int				g_elapsed_cycles		= 0;
packet			g_command				= NULL;

// Pinout
const int		PINS_A					[NUM_MOCS] = { 1, 7, 11, 17, 15, 13 };
const int		PINS_B					[NUM_MOCS] = { 3, 2, 8, 16, 14, 12 };
const int		PINS_PWM				[NUM_MOCS] = { INT_MAX, 4, 5, 10, 9, 6 };
const int		PINS_AI					[NUM_MOCS] = { INT_MAX, INT_MAX, INT_MAX, A8, A7, A6 };

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
