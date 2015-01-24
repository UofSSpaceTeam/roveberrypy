/*=======================================
Simple test program for demonstrating functionality of the 
motor controllers.  Takes a analog value from the user and
writes it to the mc via pwm.
=======================================*/
char input;
String inputStr;

void setup() {
  pinMode(9,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // get a value from the serial monitor
  while(Serial.available())
  {
    input = Serial.read();
    inputStr += input;
    delay(2);
  }
  //convert input string to int and write to mc
  if(inputStr > 0)
  {
   int num = inputStr.toInt();
   Serial.println(num);
   inputStr = "";
   analogWrite(9,num);
  }
  
}
