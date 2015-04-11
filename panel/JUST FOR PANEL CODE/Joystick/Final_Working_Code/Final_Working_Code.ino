int analogPin2 = A1; 
int analogPin0 = A0;    // potentiometer wiper (middle terminal) connected to analog pin 3
                        // outside leads to ground and +5V
int valA1 = 0;          // Y-Axis
int valA0 = 0;          // X-Axis
String OldStr = "Word";
String NewStr = "Word";

void setup()
{
  Serial.begin(9600);          //  setup serial
}

void loop() //The Serial.Println Statements in the code are if we want this to continuously check the statements.
{
  valA1 = analogRead(analogPin2);    // read the input pin
  valA0 = analogRead(analogPin0);
    
    if (valA1 > 900) {
//      Serial.println("Up");
      NewStr = "Up";
    }
    else if (valA1 < 600) {
//      Serial.println("Down");
      NewStr = "Down";
    }
    else if (valA0 > 900) {
//      Serial.println("Right");
      NewStr = "Right";
    }
    else if (valA0 < 600) {
//      Serial.println("Left");
      NewStr = "Left";
    }
    else {
 //     Serial.println("Stationary");
      NewStr = "Stationary";
    }
  if (OldStr != NewStr){
    Serial.println(NewStr);
  }
    OldStr = NewStr;
}

