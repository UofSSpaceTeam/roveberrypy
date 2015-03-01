// Written by Jordan Kubica for CME 495 project, 2014-2015
// Test code for slider speed calculation

// pin connections
#define SLIDER_PWM 6
#define SLIDER_A 7
#define SLIDER_B 4
#define LEFT_LIMIT 2
#define RIGHT_LIMIT 3

// function prototypes
void sliderLeft();
void sliderRight();
void sliderStop();

enum {STOPPED, LEFT, RIGHT} sliderDirection;

void setup()
{
	// configure I/O
	pinMode(SLIDER_A, OUTPUT);
	pinMode(SLIDER_B, OUTPUT);
	pinMode(SLIDER_PWM, OUTPUT);
	pinMode(LEFT_LIMIT, INPUT_PULLUP);
	pinMode(RIGHT_LIMIT, INPUT_PULLUP);
	
	// initialize output states
	sliderStop();
	
	// set up serial port
	Serial.begin(9600);
	
	// run test
	Serial.println("Starting...");
	sliderLeft();
	while(digitalRead(LEFT_LIMIT) == HIGH);
	sliderRight();
	unsigned long startTime = millis();
	while(digitalRead(RIGHT_LIMIT) == HIGH);
	sliderStop();
	unsigned long endTime = millis();
	Serial.print("Right traverse: ");
	Serial.println(endTime - startTime);
	sliderLeft();
	startTime = millis();
	while(digitalRead(LEFT_LIMIT) == HIGH);
	sliderStop();
	endTime = millis();
	Serial.print("Left traverse: ");
	Serial.println(endTime - startTime);
}

void loop()
{
	delay(1000);
}

void sliderLeft()
{
	if(digitalRead(LEFT_LIMIT) == HIGH)
	{
		digitalWrite(SLIDER_A, HIGH);
		digitalWrite(SLIDER_B, LOW);
		digitalWrite(SLIDER_PWM, HIGH);
		sliderDirection = LEFT;
	}
}

void sliderRight()
{
	if(digitalRead(RIGHT_LIMIT) == HIGH)
	{
		digitalWrite(SLIDER_A, LOW);
		digitalWrite(SLIDER_B, HIGH);
		digitalWrite(SLIDER_PWM, HIGH);
		sliderDirection = RIGHT;
	}
}

void sliderStop()
{
	digitalWrite(SLIDER_PWM, LOW);
	digitalWrite(SLIDER_A, LOW);
	digitalWrite(SLIDER_B, LOW);
	sliderDirection = STOPPED;
}







