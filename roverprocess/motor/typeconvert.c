#include "typeconvert.h"

unsigned char itouc(int i){
	return (unsigned char)i;
}
unsigned int itoui(int i){
	return (unsigned int)i;
}

uint8_t itoui8(int i){
	return (uint8_t)i;
}

int int32tobytes1(int i){
	return (i>>24)&0xFF;
}

int int32tobytes2(int i){
	return (i>>16)&0xFF;
}

int int32tobytes3(int i){
	return (i>>8)&0xFF;
}

int int32tobytes4(int i){
	return i&0xFF;
}

void buffer_get_int32(const uint8_t *buffer, int32_t index) {
	int32_t res =	((uint32_t) buffer[index]) << 24 |
					((uint32_t) buffer[index + 1]) << 16 |
					((uint32_t) buffer[index + 2]) << 8 |
					((uint32_t) buffer[index + 3]);
	printf("%d",res);
}
