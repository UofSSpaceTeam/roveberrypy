#include "position_constraint.h"
#include <stdlib.h>

PositionConstraint* new_PositionConstraint(const float MIN, const float MAX){
	PositionConstraint* temp = malloc(sizeof(PositionConstraint));
	*(float *)&temp->MAX = MAX;
	*(float *)&temp->MIN = MIN;
	return temp;
}



