#include "../data_types.h"
#include <stdio.h>
#include <math.h>
int main(){
	/* run tests on data types */
	
	int numPassed;
	
	/* Log tests */
	int* l_return;
	int i;
	Log* testLog;
	
	/* first PositionReading */
	
	PositionReading* reading1 = NULL;
	PositionReading* reading2 = NULL;
	PositionConstraint* c1 = NULL;
	numPassed = 0;
	
	printf("Running Data Types Test...\n");
	
	reading1 = new_PositionReading(132.4, 14.625);
	reading2 = new_PositionReading(152, 15.324);
	
	/* Test instantiation */
	if(fabs(getTime(reading1) - 14.625) < 0.0001 
		&& fabs(getTime(reading2) - 15.324) < 0.001
		&& fabs(getPosition(reading1) - 132.4) < 0.001
		&& fabs(getPosition(reading2) - 152) < 0.001 ){
		numPassed = numPassed + 1;
	} else {
		printf("ERROR: in position_reading::getTime\n");
	}
	
	/* Test difference function*/
	if(fabs(getTimeDifference_s(reading2, reading1) - 0.699) < 0.0001 
		&& fabs( getTimeDifference_ms(reading2, reading1) - 699) < 0.001 )
	{
		numPassed = numPassed + 1;	
	} else {
		printf("ERROR: in position_reading::getTimeDifference\n");
	}
	
	if( fabs(getPositionDifference(reading2, reading1) - 19.6) < 0.001){
		numPassed = numPassed + 1;
	} else {
		printf("ERROR: in position_reading::getPositionDifference\n");
	}
	
	/* print if position_reading was successful */
	if(numPassed == 3){
		printf("\nRESULT: PositionReading is working as expected.\n");
	} else {
		printf("RESULT: PositionReading test encountered errors.\n");
	}
	
	/* test position constraint */
	numPassed = 0;
	
	c1 = new_PositionConstraint(42.3, 352.1);
	
	if(fabs(c1->MIN - 42.3) < 0.0001 && fabs(c1->MAX - 352.1) < 0.0001){
		printf("\nRESULT: PositionConstraint is working as expected.\n");
	} else {
	printf("\nRESULT: PositionConstraint test encountered errors.\n");
	}	
	
	// Log tests
	init_Log(&testLog, sizeof(int), 5);
	
	append_Log(testLog, 1);
	append_Log(testLog, 2);
	append_Log(testLog, 3);
	append_Log(testLog, 4);
	append_Log(testLog, 5);
	append_Log(testLog, 6);
	append_Log(testLog, 7);
	append_Log(testLog, 8);
	append_Log(testLog, 9);
	
	read_Log(testLog, &l_return);
	if(l_return[0] == 9
		&& l_return[1] == 8
		&& l_return[2] == 7
		&& l_return[3] == 6
		&& l_return[4] == 5 ){
		printf("RESULT: Log is working as expected");
	} else {
		printf("RESULT: Errors were encountered in Log");	
	}
	
	free(l_return);
	free(testLog);
	return 0;
	
	
	return 0;
}