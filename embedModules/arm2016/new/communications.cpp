
#include <Wire.h>
#include "communications.h"

kin_packet::kin_packet() {
	type = INVERSE_KIN;
}

manual_packet::manual_packet() {
	type = MANUAL;
}




void receiveCommand(int count) {
	while(Wire.available()) {
		//read in data
		Ecommand_type cmd_type = Wire.read();
		if(cmd_type == MANUAL) {
			//read datafor maual packet
			manual_packet p;
			for(int offset=1; offset<sizeof(manual_packet); ++i) {
				// read in middle bytes
				*(p + offeset) = Wire.read();
			}
			//checksumm
			int received_checksum = 0;
			for(int offset=1; offset<sizeof(manual_packet); ++i) {
				// read in middle bytes
				received_checksum += *(p + offset);
			}
			if(received_checksum == Wire.read()) {
				//packet data successfull
				return p;
			} else {
				// packet data unreliable
				return null;
			}
		}

	}
}
