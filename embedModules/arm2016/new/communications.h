
enum Ecommand_type {MANUAL, INVERSE_KIN};

struct packet {
	Ecommand_type type;
	uint8_t checksum;

};

struct kin_packet: packet {
	int8_t position[3]; //x, y, z
};

struct manual_packet: packet {
	int8_t velocity[6];
};


void recieveCommand(int count);
