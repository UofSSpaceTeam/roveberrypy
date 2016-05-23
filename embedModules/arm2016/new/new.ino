#include "arm2016.h"
#include "arm2016_initialize.h"
#include "arm2016_serialdebug.h"

// L2 : blue: wiper, yellow: gnd, white: 5v
// L1 : blue : 5v, yellow : wiper, white: gnd, wiper->gnd resistor = 4.7k

#include <Metro.h>
/*
	comms
	feedback
	control
	*/
Metro commsTimer = Metro(PERIOD_COMM_TASK);
Metro feedbackTimer = Metro(PERIOD_FEEDBACK_TASK);
Metro controlTimer = Metro(PERIOD_CONTROL_TASK);


void setup() {
  Serial.begin(9600);
  delay(1000);
  Serial.println("initializing");
	arm2016_init();
  Serial.println("initilizeing done");
  Serial.println("Remember to set terminal to \"No line ending\" for serial command line");
}


void loop() {
	if(commsTimer.check() == 1) {
    if(g_command_received) {
      parseCommand(g_command);
      g_command_received = false;
    }
	}
	if(feedbackTimer.check() == 1) {
    updateFeedback();
    updateControllers();
	}
}


void serialEvent() {
  String buf = "";
  while(Serial.available()) {
    buf += (char)Serial.read();
  }
  char s[20];
  buf.toCharArray(s, 20);
  ReadSerialCommand(s);
}
