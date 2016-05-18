#ifndef ARM2016_VARS
#define ARM2016_VARS

#include "arm2016_types.h"

////////////////////////////////////////////////////////////////////////////////
//							TASK PERIOD DEFINITIONS
////////////////////////////////////////////////////////////////////////////////
#define 	PERIOD_CONTROL_TASK			100
#define 	PERIOD_FEEDBACK_TASK		100
#define 	PERIOD_COMM_TASK			100

////////////////////////////////////////////////////////////////////////////////
//							GENERAL SIZING DEFINITIONS
////////////////////////////////////////////////////////////////////////////////
#define 	POSITION_LOG_DEPTH 			4
#define 	NUM_MOCS 					6
#define 	LOG_SIZE					POSITION_LOG_DEPTH*NUM_MOCS

////////////////////////////////////////////////////////////////////////////////
//							SHARED GLOBALS
////////////////////////////////////////////////////////////////////////////////
#define MAX_POS 1023
#define DEF_POS 512
#define MIN_POS 0

int 			g_destination	[NUM_MOCS]; 											// destinations
int 			g_position_log	[POSITION_LOG_DEPTH][NUM_MOCS] = {						// log of positions
	{DEF_POS, DEF_POS, DEF_POS, DEF_POS, DEF_POS, DEF_POS},
	{DEF_POS, DEF_POS, DEF_POS, DEF_POS, DEF_POS, DEF_POS},
	{DEF_POS, DEF_POS, DEF_POS, DEF_POS, DEF_POS, DEF_POS},
	{DEF_POS, DEF_POS, DEF_POS, DEF_POS, DEF_POS, DEF_POS},
	{DEF_POS, DEF_POS, DEF_POS, DEF_POS, DEF_POS, DEF_POS},
	{DEF_POS, DEF_POS, DEF_POS, DEF_POS, DEF_POS, DEF_POS}
};
int				(*g_position)	[NUM_MOCS] 	= g_position_log;							// current positions
double			g_velocity		[NUM_MOCS];												// current velocities
int				g_duty_cycle	[NUM_MOCS];												// current duty-cycles
int				g_elapsed_cycles			= 0;										// number of control task cycles elapsed
																						// since last new movement command

////////////////////////////////////////////////////////////////////////////////
//							CONTROL GLOBALS
////////////////////////////////////////////////////////////////////////////////
// n/a

////////////////////////////////////////////////////////////////////////////////
//							FEEDBACK GLOBALS
////////////////////////////////////////////////////////////////////////////////
#define 		ANALOG_READ_NSAMPLES 11													// number of samples used for reading position
#define 		SMOOTH_DIFF_SIZE 	POSITION_LOG_DEPTH									// order of smooth-differentiator
int 			analog_read_samples	[ANALOG_READ_NSAMPLES];									// work array for finding median of dataset
const double 	leading_coeff 		= 1.0/(8.0 * ((double) PERIOD_FEEDBACK_TASK / 1000.0));	// normalizing coefficient
const double 	term_coeffs			[SMOOTH_DIFF_SIZE] = { 1.0, 2.0, -2.0, -1.0 };			// term coefficients

////////////////////////////////////////////////////////////////////////////////
//							COMM'S GLOBALS
////////////////////////////////////////////////////////////////////////////////
packet			g_command					= NULL;
#define		I2C_ADDRESS 0x07

////////////////////////////////////////////////////////////////////////////////
//							DCM GLOBALS/CONFIG
////////////////////////////////////////////////////////////////////////////////
#define 		DCM_SIZE 					6
#define 		MAX_DC 						255.0

const double 	TIME_RAMP_UP_MS 			= 300;  									//  Time of ramp-up
const double 	DCM_PERIOD_MS 				= PERIOD_CONTROL_TASK;						//  Period of duty-cycle manager
const double 	DCM_MIN_VEL_INC 			= MAX_DC * DCM_PERIOD_MS / TIME_RAMP_UP_MS;	// size of below min velocity dc increment
const double 	DCM_rd_dists	[DCM_SIZE] 	= { 50, 50, 50, 50, 50, 50 };				// distance to begin ramp-down
const double 	DCM_min_vels	[DCM_SIZE] 	= { 10, 10, 10, 10, 10, 10 };				// minimum allowable velocity
const double  	DCM_tolerance	[DCM_SIZE] 	= { 5, 5, 5, 5, 5, 5 };						// 'close enough' tolerance
double  		DCM_dists		[DCM_SIZE];												// work array used internally by dcm
double  		DCM_vels		[DCM_SIZE];												// work array used internally by dcm
ERFStage 		DCM_stages		[DCM_SIZE]; 											// stages of movements
bool			g_ramping_enabled			= true;


////////////////////////////////////////////////////////////////////////////////
// 								PINOUT
////////////////////////////////////////////////////////////////////////////////
#define 		NO_PWM 								0
#define 		NO_FB 								0
#define 		DIRECTION_NORMAL 					1
#define			DIRECTION_REVERSED 					-1
const int		PINS_A					[NUM_MOCS]	= { 1, 7, 11, 17, 15, 13 };				// direction A pins
const int		PINS_B					[NUM_MOCS] 	= { 3, 2, 8, 16, 14, 12 };				// direction B pins
const int		PINS_PWM				[NUM_MOCS] 	= { NO_PWM, 4, 5, 10, 9, 6 };			// PWM pins
const int		PINS_AI					[NUM_MOCS] 	= { NO_FB, NO_FB, NO_FB, A8, A7, A6 };	// analog-input pins
const int		DIRECTION_MASK			[NUM_MOCS] 	= {										// mask for hardware direction
	DIRECTION_NORMAL,
	DIRECTION_NORMAL,
	DIRECTION_NORMAL,
	DIRECTION_NORMAL,
	DIRECTION_NORMAL,
	DIRECTION_NORMAL
};

#endif
