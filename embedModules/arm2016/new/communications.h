#ifndef COMMUNICATIONS
#define COMMUNICATIONS

enum Ecommand_type {MANUAL, INVERSE_KIN};

struct packet {
	Ecommand_type type;
	int8_t position[3]; //x, y, z
	int8_t velocity[6]; // speed and direction of each motor
	uint16_t checksum();

};


void recieveCommand(int count);

#endif
