#ifndef ARM2016_COMMS
#define ARM2016_COMMS

#include <Wire.h>
#include "arm2016_vars.h"
#include "arm2016_types.h"

/**
 * Recieve a command packet over i2c and updates global
 * command packet if the checksum matches.
 * Must be initialized with Wire.onReceive
 */
void recieveCommand(int count);
void sendPosition();
void parseCommand(packet command);


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
	return sum % 256;
}


void receiveCommand(int count) {
  byte in_bytes[count]; // buffer
  int i = 0;
  packet in_command;

  //read in all bytes into buffer
  while (Wire.available()) {
    in_bytes[i] = (int8_t)Wire.read();
    i++;
  }
  if(in_bytes[0] == GET_FEEDBACK) {
     sendPosition();
  } else {

#ifdef COMMS_DEBUG
     Serial.println("incomming packet:");
     for (int i = 0; i < count; i++) {
       Serial.println(in_bytes[i]);
     }
     Serial.println("end of packet");
#endif
     //move buffer to new packet
     in_command.type = (Ecommand_type)in_bytes[0];
	  for (int i = 7; i <= 13; i++) {
		  in_command.duty_cycle[i - 7] = in_bytes[i];
	  }
	  for (int i = 1; i < 6; i += 2) {
		 in_command.position[(i - 1) / 2] = 0x00FF & in_bytes[i]; //lsb
		 in_command.position[(i - 1) / 2] |= 0xFF00 & (in_bytes[i + 1] << 8); //msb
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
       g_command = in_command;
       g_command_received = true;
#ifdef COMMS_DEBUG
       Serial.println("Packet recieved");
#endif

     } else {
       // bad packet; do nothing
#ifdef COMMS_DEBUG
       Serial.println("Got bad packet");
       Serial.printf("(Expected chksum: %d)", in_bytes[count-1]);
#endif
     }

   }
}

void sendPosition() {
	//transmit position feedback data to the rover
#ifdef COMMS_DEBUG
	Serial.println("Got a position feedback request");
#endif
	for(int i=3; i<=4; ++i) {
#ifdef COMMS_DEBUG
		Serial.println(*(g_position)[i]);
#endif
		Wire.write(((*g_position)[i]) & 0x00FF); //lsb
		Wire.write((((*g_position)[i]) & 0xFF00) >> 8); //msb
	}

}


//command parsing
void parseCommand(packet command) {
	g_ivk_controller = command.type == INVERSE_KIN_CON;
	if(command.type == MANUAL) { // actions for manual command
		Serial.println("manual command get");
		g_ivk_controller = false;
		for(int i=0; i<NUM_MOCS; i++) {
			g_duty_cycle[i] = 2*command.duty_cycle[i];
		}
		g_ramping_enabled = false;
	} else if(command.type == INVERSE_KIN_GUI) {
		for(int i=0; i<3; i++) {
			g_destination[i] += command.position[i];
		}

		g_ramping_enabled = true; // ramping may be anoying for joystick controll
	} else if(command.type == INVERSE_KIN_CON) {
		if(command.position[0] > 0) { // set radius flag
			g_inc_radius = 1;
		} else if(command.position[0] < 0) {
			g_inc_radius = -1;
		} else {
			g_inc_radius = 0;
		}
		if(command.position[1] > 0) { // set altitude flag
			g_inc_altitude = 1;
		} else if(command.position[1] < 0) {
			g_inc_altitude = -1;
		} else {
			g_inc_altitude = 0;
		}


		g_ivk_controller_scale = max(abs(command.position[0])/255,
				abs(command.position[1])/255);
	}
}


#endif
