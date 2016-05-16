#ifndef ARM2016_COMMS
#define ARM2016_COMMS

#include <Wire.h>


enum Ecommand_type {MANUAL, INVERSE_KIN};

struct packet {
	Ecommand_type type;
	int8_t position[3]; //x, y, z
	int8_t velocity[6]; // speed and direction of each motor
	uint16_t checksum();

};


void recieveCommand(int count);


/**
 * Calculate packet checksum by adding data elements together.
 */
uint16_t packet::checksum() {
	uint16_t sum = 0;
	for(int i=0; i<3; ++i) {
		sum += position[i];
	}
	for(int i=0; i<6; ++i) {
		sum += velocity[i];
	}
	return sum;
}

/**
 * Recieve a command packet over i2c and updates global
 * command packet if the checksum matches.
 * Must be initialized with Wire.onReceive
 */
void receiveCommand(int count) {
	while(Wire.available()) {
		//read in data
		packet in_command;
		in_command.type = Wire.read();

		for(int i=1; i<3; ++i) {
			// read in position data
			in_command.position[i] = Wire.read();
		}
		for(int i=1; i<6; ++i) {
			// read in velocity data
			in_command.velocity[i] = Wire.read();
		}

		if(command.checksum() == Wire.read()) {
			//packet data successfull
			command = in_command
		} else {
			// packet data unreliable
		}

	}
}


#endif
