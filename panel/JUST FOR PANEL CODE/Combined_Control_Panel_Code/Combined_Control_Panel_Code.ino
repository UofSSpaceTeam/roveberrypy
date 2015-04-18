#include <Keypad.h>
//Download keypad.h into "arduinio\libraries\" and go to Sketch - Import Library - Keypad

//Resistors on keypad pin 7, 6, 4, 2!!!!!!!!!!!!!!!!!!!!!!!

  //four rows and three columns in "matrix"
  const byte ROWS = 4;
  const byte COLS = 3;
 
 char keys[ROWS][COLS] = {
   {'1', '2', '3'},
   {'4', '5', '6'},
   {'7', '8', '9'},
   {'#', '0', '*'} //# and * flipped to work with our keypad.
 };
 
 //Connects the row of pinouts of the keypad
 byte rowPins[ROWS] = {A9,A5,A4,A7}; 
 //Connects to the column pinouts of the keypad
 byte colPins[COLS] = {A8,A10,A6}; 
 
 //Keypad mykeypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );
// Keypad customKeypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, cols); 
Keypad kpd = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

/////////////////////////////////////////////////////////////////////////////////

//Pin Number: Button/Switch
//2:  Switch 1
//3:  Switch 2
//4:  Switch 3
//5:  Switch 4
//6:  Telemetry Control 1
//7:  Telemetry Control 2
//8:  Telemetry Control 3
//9:  Telemetry Control 4
//10: Telemetry Control 5
//11: Telemetry Control 6
//12: Timer
//13: GPS

int inPin[] = {2,3,4,5,6,7,8,9,10,11,12,13};
int newstate;
const int pinCount = 12;
int state[pinCount];
int thisPin = 0;

/////////////////////////////////////////////////////////////////////////////

int analogPin2 = A1; 
int analogPin0 = A0;    // potentiometer wiper (middle terminal) connected to analog pin 3
                        // outside leads to ground and +5V
int valA1 = 0;          // Y-Axis
int valA0 = 0;          // X-Axis
String OldStr = "Word";
String NewStr = "Word";

///////////////////////////////////////////////////////////////////////////

int potPin1 = A2;    // select the input pin for the potentiometer
int potPin2 = A3;
int potPin3 = A11;
int P1val = 1;       // variable to store the value coming from the sensor
int P2val = 1;
int P3val = 1;

void setup(){
for (int i = 0; i < pinCount; i++)
  {
    pinMode(inPin[i],INPUT_PULLUP);
  }
  Serial.begin(9600);
}


void loop()
/////////////// KEYPAD ////////////////
{
  char key = kpd.getKey();
   
  if (key != NO_KEY){
  }
////////////// SWITCH /////////////////
   for(int i = 0; i < pinCount; i++)
  {
    int reading = digitalRead(inPin[i]);
    if (reading == HIGH)
    {
      newstate = 0;
    }
    else
    {
      newstate = 1;
    }
    if (newstate != state[i])
    {
      delay(100);
      state[i] = newstate;
    } 
  }
///////////// JOYSTICK ///////////////
{
  valA1 = analogRead(analogPin2);    // read the input pin
  valA0 = analogRead(analogPin0);    //The Serial.println Statements in the code are if we want this to continuously check the statements
    
    if (valA1 > 900) {               //UP
      NewStr = "U";
    }
    else if (valA1 < 600) {          //DOWN
      NewStr = "D";
    }
    else if (valA0 > 900) {          //RIGHT
      NewStr = "R";
    }
    else if (valA0 < 600) {          //LEFT
      NewStr = "L";
    }
    else {                           //STATIONARY
      NewStr = "S";
    }
    OldStr = NewStr;
 }
/////////////// DIALS ////////////////
  {
  P1val = analogRead(potPin1)+1;    // read the value from the sensor
  P2val = analogRead(potPin2)+1;
  P3val = analogRead(potPin3)+1;
  }
/////////////// PRINT ////////////////
Serial.print("$");
for(int i = 0; i < pinCount; i++){
  Serial.print(state[i]);
  Serial.print(",");
}
Serial.print(key);
Serial.print(",");
Serial.print(NewStr);
Serial.print(",");
  {
for(int a=1; a < 4 - log10(P1val); a++)
Serial.print('0');
Serial.print(P1val,DEC);
  }
Serial.print(",");
  {
for(int b=1; b < 4 - log10(P2val); b++)
Serial.print('0');
Serial.print(P2val,DEC);
  }
Serial.print(",");
  {
for(int c=1; c < 4 - log10(P3val); c++)
Serial.print('0');
Serial.print(P3val,DEC);
  }
Serial.println("&");
}
