#include "packet.h"


uint8_t* PackSendPayload( uint8_t* payload, int lenPay) {
	uint16_t crcPayload = crc16(payload, lenPay);
	
	int count = 0;
	uint8_t messageSend[256];

	if (lenPay <= 256)
	{
		messageSend[count++] = 2;
		messageSend[count++] = lenPay;
	}
	else
	{
		messageSend[count++] = 3;
		messageSend[count++] = (uint8_t)(lenPay >> 8);
		messageSend[count++] = (uint8_t)(lenPay & 0xFF);
	}
	memcpy(&messageSend[count], payload, lenPay);

	count += lenPay;
	messageSend[count++] = (uint8_t)(crcPayload >> 8);
	
	messageSend[count++] = (uint8_t)(crcPayload & 0xFF);
	
	messageSend[count++] = 3;
	messageSend[count] = NULL;
    for(int i = 0; i < count; i++)
		printf("%x,", messageSend[i]);
	return messageSend;
}