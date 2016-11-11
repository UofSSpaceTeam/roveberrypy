from ctypes import *
from libc.stdlib cimport malloc, free
from libc.stdint cimport *
from libc.stdio cimport printf
import serial

cdef extern from "crc.c":
    unsigned short crc16(unsigned char*, unsigned int)

cdef extern from "typeconvert.c":
    unsigned char itouc(int)
    unsigned int itoui(int)
    uint8_t itoui8(int)
    int int32tobytes1(int)
    int int32tobytes2(int)
    int int32tobytes3(int)
    int int32tobytes4(int)
    void buffer_get_int32(const uint8_t *buffer, int32_t index)

cdef extern from "packet.c":
    uint8_t* PackSendPayload( uint8_t*, int)

cdef extern from "print.c":
    void printUint8(uint8_t)

def pycrc16(buffer, int len):
    cdef unsigned char* c_buffer = <unsigned char *>malloc(len * sizeof(unsigned char))
    for i in range(0,len):
        c_buffer[i] = itouc(buffer[i])
    cdef unsigned int c_len = itoui(len)
    return c_ushort(crc16(c_buffer, c_len))	
	
def pySendPacket( payload, len):
    cdef uint8_t* c_payload = <uint8_t *>malloc(len * sizeof(uint8_t))
    for i in range(0,len):
        c_payload[i] = itoui8(payload[i])
    PackSendPayload( c_payload, len)
	
def pyint32tobytes(i):
    buffer = []
    buffer.append(int32tobytes1(i))
    buffer.append(int32tobytes2(i))
    buffer.append(int32tobytes3(i))
    buffer.append(int32tobytes4(i))
    print(buffer)
    buffer_get_int32(bytes(buffer),0)
	
    return buffer	
		



