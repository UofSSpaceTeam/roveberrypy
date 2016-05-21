#include "arm2016.h"
#include "arm2016_initialize.h"
#include "arm2016_vars.h"
#include "arm2016_serialdebug.h"

// L2 : blue: wiper, yellow: gnd, white: 5v
// L1 : blue : 5v, yellow : wiper, white: gnd, wiper->gnd resistor = 4.7k

#include <Metro.h>
/*
	comms
	feedback
	control
	*/
Metro commsTimer = Metro(1000);
Metro feedbackTimer = Metro(1500);
Metro controlTimer = Metro(500);


void setup() {
  Serial.begin(9600);
  delay(1000);
  Serial.println("initializing");
	arm2016_init();
  Serial.println("initilizeing done");
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
	}
	if(controlTimer.check() == 1) {
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



