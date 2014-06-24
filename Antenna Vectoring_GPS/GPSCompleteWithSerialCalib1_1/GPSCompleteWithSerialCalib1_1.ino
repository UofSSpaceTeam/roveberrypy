#include <TinyGPS.h>
#include <Servo.h>

/*
Currently, the connected gps plays the part of the base.  The rover is set arbitrarily using coordinates, for testing.
Servo is attached on pin 9, GPS is on Serial2.  There is lots of print statements for troubleshooting that can be 
removed.  There is another gps lib (TinyGPSPlus) that can be used to incorporate doubles because the Arduino Due can
handle doubles.  That only needs to be done if we want higher precision of the values, but the angle has to be rounded
to an integer value anyways for the servo.

Work that needs to be done:
  - Integrate the 2nd gps
    * receive gps data from a second unit
    * use the received data instead of the arbitrarily assigned points
  - Debug statements need to be deleted or commented out (any Serial.print or Serial.println statement)
*/
//gpsRover connects to Serial2


TinyGPS gpsBase;
TinyGPS gpsRover;
Servo antennaServo;
bool calibrated1 = false;// Used for 2 different phases of the initial calibration
bool calibrated2 = false;
int calibrationAngle;  // This is the angle that must be added to the angle from north to get the servo angle
int roverMoveDelay = 0;  //Used for assigning arbitrary points on a delay for testing the servo

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial2.begin(9600);
  antennaServo.attach(9);
}

void loop() {
  // put your main code here, to run repeatedly: 
  int servoAngle;
  if (calibrated1 == false){
    calibrationAngle = calibrate(); //Only runs calibrate the first time.  Calibrated1 can be made false to recalibrate later
  }
  bool newData = false;
  while (Serial2.available()){
    char c = Serial2.read();
    if (gpsBase.encode(c)){
      newData = true;
    }
  }
  if (newData){
    float roverLon, roverLat;
    float baseLon, baseLat;
    unsigned long age;
    float roverAngle;
    //This is used for explicitly feeding coordinates to roverLat and roverLon for testing
    if (roverMoveDelay < 50){
      roverLat = 52.12;
      roverLon = -106.669;
    }
    else if (roverMoveDelay < 100){
      roverLat = 52.13;
      roverLon = -106.670;
    }
    else if (roverMoveDelay < 150){
      roverLat = 52.14;
      roverLon = -106.671;
    }
    else if (roverMoveDelay < 200){
      roverLat = 52.15;
      roverLon = -106.672;
    }
    else if (roverMoveDelay < 250){
      roverLat = 52.16;
      roverLon = -106.673;
    }
    else if (roverMoveDelay < 300){
      roverLat = 52.17;
      roverLon = -106.674;
    }    
    
    gpsBase.f_get_position(&baseLat, &baseLon, &age);
    //Add code here for retrieving the roverLat and roverLon
    //Include a test for proper data such as below if the data is verified before retrieval
    
    if (baseLat == TinyGPS::GPS_INVALID_F_ANGLE || baseLon == TinyGPS::GPS_INVALID_F_ANGLE){
      Serial.println("GPS error");
    }
    else {
        roverMoveDelay = roverMoveDelay + 5; //only used for testing, can be removed once we have 2nd GPS feeding data
        roverAngle = calculateAngle(roverLat, roverLon, baseLat, baseLon);
        Serial.print("The angle(from north) is:  ");//all Serial.print statements are for troubleshooting only
        Serial.println(roverAngle);
        Serial.println(calibrationAngle);
        
        float angle = roverAngle - calibrationAngle;
        Serial.print("Servo angle:  ");
        Serial.println(angle);
        servoAngle = angle + 0.5;
        
        //if the rover goes out of the limits of the servos movement it stops trying to turn that far
        //Perhaps add a message to the user indicating that the rover is beyond the turning range
        if (servoAngle < 20){
          servoAngle = 20;
        }
        if (servoAngle > 160){
          servoAngle = 160;
        }
        Serial.print("The angle(of the servo) is:  ");
        Serial.println(servoAngle);
        antennaServo.write(servoAngle);  //moves the servo to the determined angle
    }
  }
}

float calculateAngle(double roverLat, double roverLon, double baseLat, double baseLon){
  roverLon = (roverLon * 71)/4068;//conversion to radians
  roverLat = (roverLat * 71)/4068;
  baseLon = (baseLon * 71)/4068;
  baseLat = (baseLat * 71)/4068;
  double dLon = roverLon - baseLon;
  double y = sin(dLon) * cos(roverLat);
  double x = cos(baseLat) * sin(roverLat) - sin(baseLat) * cos(roverLat) * cos(dLon);
  float angle = atan2(y, x);
  angle = (angle * 4068)/71;
  return angle;
}

//Calibration Function
//Input servo angles to the program explicitly using serial monitor
//when the servo is pointed towards the roverGPS satisfactorily enter 'y' (without quotation marks)

int calibrate(){
  Serial.println("beginning calibration");
  char incomingByte[3];
  int servoAngle = 0;
  int calibrationAngle = 0;
  calibrated1 = false;
  while (calibrated1 == false){
    //Serial.println("calibrated1 = false");
    int len = 0;
    while (Serial.available() > 0) {
      incomingByte[len] = Serial.read();
      len++;
      delay(100);
    }
    if (incomingByte[0] == 'Y' || incomingByte[0] == 'y'){
      calibrated1 = true;
      Serial.println("calibrated1 = true");
    }
    else if (incomingByte[0] >= '0' && incomingByte[0] <= '9'){
      servoAngle = 0;
      for (int i = 0; i < len; i++){
        int increment = (int(incomingByte[i]) - 48) * pow(10, len-(1+i)); //converts number entered as characters into usable int value
        servoAngle = servoAngle + increment;
      }
      if (servoAngle >= 20 && servoAngle <= 160){
        antennaServo.write(servoAngle);
        Serial.print("Servo angle is:  ");
        Serial.println(servoAngle);
      }
      else{
        Serial.println("Angle outside accepted range (20 - 160)");
        Serial.println(incomingByte);
        Serial.println(servoAngle);
      }
      for (int i = 0; i < 3; i++){
        incomingByte[i] = 'g';
      }
    }
  }
  int i = 0;
  while(calibrated2 == false){
    Serial.println("Checking GPS");
    bool newData = false;
    while (Serial2.available()){
      char c = Serial2.read();
      if (gpsBase.encode(c)){
        newData = true;
        Serial.println("GPS data found.");
      }
    }
    if (newData){
      float roverLon, roverLat;
      float baseLon, baseLat;
      unsigned long age;
      gpsBase.f_get_position(&baseLat, &baseLon, &age);
      if (baseLat == TinyGPS::GPS_INVALID_F_ANGLE || baseLon == TinyGPS::GPS_INVALID_F_ANGLE){
        Serial.println("GPS error");
      }
      else{
        i++;
        if (i > 20){
          float roverAngle;
          roverLat = 52.12;
          roverLon = -106.669;
          roverAngle = calculateAngle(roverLat, roverLon, baseLat, baseLon);
          calibrated2 = true;
          float angleTemp = roverAngle - servoAngle;
          float roundingValue = 0.5;
          if (angleTemp < 0){
            roundingValue = -0.5;
          }
          calibrationAngle = angleTemp + roundingValue;
          Serial.println("roverAngle  |  servoAngle  |  angleTemp  |  calibrationAngle\n------------------------------------------------------------");
          Serial.print("    ");
          Serial.print(roverAngle);
          Serial.print("   |    ");
          Serial.print(servoAngle);
          Serial.print("     |     ");
          Serial.print(angleTemp);
          Serial.print("     |     ");
          Serial.println(calibrationAngle);
        }
      }
    }
  }
  Serial.print(calibrationAngle);
  Serial.print(" sent.");
  return calibrationAngle;
}
    
      
      
