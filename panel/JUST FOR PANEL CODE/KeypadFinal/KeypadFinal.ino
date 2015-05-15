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
 byte rowPins[ROWS] = {A9,A6,A4,A7};//{A9,A5,A4,A7}; 
 //Connects to the column pinouts of the keypad
 byte colPins[COLS] = {A8,A10,A5};//{A8,A10,A6}; 
 
 //Keypad mykeypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );
// Keypad customKeypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, cols); 
Keypad kpd = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );


void setup() 
{
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  char key = kpd.getKey();
   
   if (key != NO_KEY){
      Serial.println(key);
   }
} 

