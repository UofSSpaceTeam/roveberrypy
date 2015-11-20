typedef struct {
int dir_pin;
int pwd_pin;
int wiper_pin;
} MotorController;


void turnon(e_Direction dir,int duty);

void turnoff();

void updateDutyCycle(int duty);

