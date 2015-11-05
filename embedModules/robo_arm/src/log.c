#include "log.h"
#include <stdlib.h>
#include <stdio.h>

void init_Log(Log** l, unsigned int t_size, unsigned int length){
	// Allocate memory for Log
	free(*l); // free whatever l is pointing to
	*l = malloc(sizeof(Log)); // allocate memory for new Log
	(*l) -> d = (void *)malloc(t_size*length); // allocate data memory
	
	// initialize properties
	(*l) -> l_size = length;
	(*l) -> l_pos = 0;
}

void append_Log(Log* l, int val){
	// step position in Log data
	if(l->l_pos > 0){
		l->l_pos = l->l_pos - 1;
	} else {
		l->l_pos = l->l_size - 1;
	}
	
	// append val to data
	*((int *)(l->d) + l->l_pos) = val;
}

void read_Log(Log* l, int** p_rtn){
	int i;
	
	// Memory managment for return pointer
	free(*p_rtn); // free memory in p_rtn if it is not already empty
	*p_rtn = malloc(sizeof(int)*l->l_size); // allocate memory for return
	
	// copy Log in order starting with most recent value appended
	for(i = 0; i < l->l_size; i++){
		*((*p_rtn) + i) = *((int *)(l->d) + (i + l->l_pos) % l->l_size);
	}
}
