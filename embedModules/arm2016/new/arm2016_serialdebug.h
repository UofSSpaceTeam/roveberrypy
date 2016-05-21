#ifndef ARM2016_SERDBG
#define ARM2016_SERDBG

#include <string.h>
#include <cstdlib>

#define ALL_MOTORS 10

enum ECommand { SET, MOVE, STOP, ERROR };

void ReadSerialCommand(char command_cstr[]) {
	ECommand command;
	char* word;
	int motor_id;
	// Begin parsing the command
	if 		(strcmp(pch, "set") == 0) 	command = SET;
	else if (strcmp(pch, "move") == 0) 	command = MOVE;
	else if (strcmp(pch, "stop") == 0) 	command = STOP;
	else 								command = ERROR;
	// Parse which motor
	if (pch != NULL) {
		if 		(strcmp(pch, "m0")  == 0) 	motor_id = 0;
		else if (strcmp(pch, "m1")  == 0) 	motor_id = 1;
		else if (strcmp(pch, "m2")  == 0) 	motor_id = 2;
		else if (strcmp(pch, "m3")  == 0) 	motor_id = 3;
		else if (strcmp(pch, "m4")  == 0) 	motor_id = 4;
		else if (strcmp(pch, "m5")  == 0) 	motor_id = 5;
		else if (strcmp(pch, "all") == 0 && command == STOP) {
			motor_id = ALL_MOTORS;
		}
		else command = ERROR;
	} else if(command == STOP) {
		motor_id = ALL_MOTORS;
	} else command = ERROR;
	// Parse additional argument
	double arg;
	pch = strtok(NULL, " ");
	if (pch != NULL) {
		arg = strtod(pch, NULL);
	}
	// Carry out the commands
	switch (command) {
	case SET:
		g_ramping_enabled = false;
		g_duty_cycle[motor_id] = arg;
		Serial.print("Setting duty-cycle of m");
		Serial.print(motor_id);
		Serial.print(": value=");
		Serial.println(arg);
		break;
	case MOVE:
		g_ramping_enabled = true;
		g_elapsed_cycles = 0;
		g_destination[motor_id] = arg;
		Serial.print("Initializing movement of m");
		Serial.print(motor_id);
		Serial.print(": destination=");
		Serial.println(arg);
		break;
	case ERROR:
		Serial.println("ERROR: There was an error in your arguments!");
		motor_id = ALL_MOTORS;
	case STOP:
		if(motor_id != ALL_MOTORS) {
			g_duty_cycle[motor_id] = 0;
			Serial.print("Stopping m");
			Serial.println(motor_id);
		} else {
			g_duty_cycle[0] = 0;
			g_duty_cycle[1] = 0;
			g_duty_cycle[2] = 0;
			g_duty_cycle[3] = 0;
			g_duty_cycle[4] = 0;
			g_duty_cycle[5] = 0;
			Serial.println("Stopping all motors");
		}
		break;
	}

}

#endif
