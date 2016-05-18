#ifndef ARM2016_COMMS
#define ARM2016_COMMS

#include <Wire.h>
#include "arm2016_vars.h"
#include "arm2016_types"

/**
 * Recieve a command packet over i2c and updates global
 * command packet if the checksum matches.
 * Must be initialized with Wire.onReceive
 */
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


void receiveCommand(int count) {
	byte in_bytes[11]; // buffer
	int i = 0;

	//read in all bytes into buffer
	while(Wire.available()) {
		in_bytes[i] = Wire.read();
		i++;
	}

	packet in_command;
	//move buffer to new packet
	in_command.type = (Ecommand_type)in_bytes[0];
	for(int i=0; i<3; i++) {
		in_command.position[i] = in_bytes[i+1];
	}
	for(int i=0; i<6; i++) {
		in_command.velocity[i] = in_bytes[i+4];
	}

	//================================
	// Debugging
#ifdef COMMS_DEBUG
	Serial.println(in_command.type);
	for(int i=0; i<3; i++) {
		Serial.println(in_command.position[i]);
	}
	for(int i=0; i<6; i++) {
		Serial.println(in_command.velocity[i]);
	}
	Serial.println(in_command.checksum());
#endif
	//===================================

	if(in_command.checksum() == in_bytes[10]) {
		// update global packet
		g_command = in_command;
#ifdef COMMS_DEBUG
		Serial.println("Packet recieved");
#endif

	} else {
		// bad packet; do nothing
#ifdef COMMS_DEBUG
		Serial.println("Got bad packet");
#endif
	}

}


#endif
