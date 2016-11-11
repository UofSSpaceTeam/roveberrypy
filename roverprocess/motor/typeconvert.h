#ifndef TYPECONVERT_H_
#define TYPECONVERT_H_

/*
 * Functions
 */
unsigned char itouc(int i);
unsigned int itoui(int i);
uint8_t itoui8(int i);
int int32tobytes1(int i);
int int32tobytes2(int i);
int int32tobytes3(int i);
int int32tobytes4(int i);

void buffer_get_int32(const uint8_t *buffer, int32_t index);
#endif /* TYPECONVERT_H_ */