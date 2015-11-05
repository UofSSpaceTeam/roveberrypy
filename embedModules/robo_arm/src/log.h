#ifndef LOG_H
#define LOG_H

typedef struct{
	void* d;
	unsigned int l_size;
	unsigned int l_pos;
} Log;

/**
 *  Create a log.
 *  @warning Allocates memory in *l.
 *  @param t_size The size of the type to be stored.
 *  @param length The number of elements in the log.
 */
void init_Log(Log** l, unsigned int t_size, unsigned int length);

/**
 *  Add a value to an integer log.
 *  @param l The log.
 *  @param val The integer to be appended in the log.
 */
void append_Log(Log* l, int val);

/**
 *  Get get log. 
 *  @warning Allocates memory in *p_rtn.
 *  @param l The integer log.
 *  @return An integer array of the data stored in the log. 
 */
void read_Log(Log* l, int** p_rtn);





#endif