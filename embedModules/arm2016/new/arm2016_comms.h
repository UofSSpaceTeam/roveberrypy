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
		sum += duty_cycle[i];
	}
	return sum;
}


void receiveCommand(int count) {
  byte in_bytes[count]; // buffer
  int i = 0;

  //read in all bytes into buffer
  while (Wire.available()) {
    in_bytes[i] = (int8_t)Wire.read();
    i++;
  }
#ifdef COMMS_DEBUG
  Serial.println("incomming packet:");
  for (int i = 0; i < count; i++) {
    Serial.println(in_bytes[i]);
  }
  Serial.println("end of packet");
#endif
  packet in_command;
  //move buffer to new packet
  in_command.type = (Ecommand_type)in_bytes[0];
  for (int i = 1; i < 6; i += 2) {
    in_command.position[(i - 1) / 2] = 0x00FF & in_bytes[i]; //lsb
    in_command.position[(i - 1) / 2] |= 0xFF00 & (in_bytes[i + 1] << 8); //msb
  }
  for (int i = 7; i <= 13; i++) {
    //we devided by 2 on the other side to fit negative numbers in
    //will mess up the checksum
    in_command.duty_cycle[i - 7] = in_bytes[i];
  }

  //================================
  // Debugging
#ifdef COMMS_DEBUG
  Serial.println("final structured packet");
  Serial.println(in_command.type);
  for (int i = 0; i < 3; i++) {
    Serial.println(in_command.position[i]);
  }
  for (int i = 0; i < 6; i++) {
    Serial.println(in_command.duty_cycle[i]);
  }
  Serial.println(in_command.checksum());
#endif
  //===================================

  if (in_command.checksum() == in_bytes[count - 1]) {
    // update global packet
    //g_command = in_command;
    //g_command_received = true;
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



//command parsing
void parseCommand(packet command) {
	if(command.type == MANUAL) { // actions for manual command
		for(int i=0; i<NUM_MOCS; i++) {
			g_duty_cycle[i] = command.duty_cycle[i];
		}
		g_ramping_enabled = false;
	} else if(command.type == INVERSE_KIN) {
		g_ramping_enabled = true;
	}
}


#endif
