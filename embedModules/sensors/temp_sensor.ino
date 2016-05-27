float temperature ;

void setup() {
  // Begin serial communications between board and computer:
  Serial.begin(9600) ;
}

void loop() {
  // Read in the resistance value of the analog signal (From 0 to 1023)
  int rawData = analogRead(A0) ;

  // Convert value to voltage by scaling between 0.0 and 5.0
  float Vout = rawData * (3.3 / 1023.0) ;

  // Datasheet says temperature roughly linear (Provides polynomial for more realistic values, look later)
  temperature = Vout/0.005 ;
  
  // Print Information to Serial Window
  Serial.print(temperature) ;
  Serial.print("\n") ;
}
