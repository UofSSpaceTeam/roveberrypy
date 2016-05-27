int decagon_pin = A9 ;
float V = 3.3 ;

//setup coefficients for curve fitting (apparent dielectric permittivity):

/*float  coef1 = 2.589*pow(10,-10) ;
float  coef2 = -5.010*pow(10,-7) ;
float  coef3 = 3.523*pow(10,-4) ;
float  coef4 = -9.135*pow(10,-2) ;
float  coef5 = 7.457 ;*/

//Setup coefficients for curve fitting (percent humidity)
//*Note: Sensor only accurate from 0% to 57%

float coef1 = 0 ;
float coef2 = 2.97*pow(10,-9) ;
float coef3 = -7.37*pow(10,-6) ;
float coef4 = 6.69*pow(10,-3) ;
float coef5 = -1.92 ;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600) ;
}

void loop() {
  // put your main code here, to run repeatedly:
  int raw_moisture_reading = analogRead(decagon_pin) ;

  //code to convert to raw voltage (in mV)
  //float mV = (raw_moisture_reading/1023.0)*950.0+300.0 ;
  //Note: Teensy uses 3.3 V as VRef by default, other boards may use different reference voltages
  float mV = raw_moisture_reading*(3.3/1.0240) ;

  //code to calibrate (curve provided in datasheet)
  float moisture_reading = 100*(coef1*pow(mV,4)+coef2*pow(mV,3)+coef3*pow(mV,2)+coef4*mV+coef5) ;
  //float moisture_reading = mV*57.0 ;

  Serial.print(moisture_reading) ;
  Serial.print("\n") ;
  delay(250) ;
}
