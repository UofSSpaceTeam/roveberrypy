#include <Wire.h>


// Stuff for LSM9DS0
#include <SPI.h> // Included for SFE_LSM9DS0 library for some timing stuff?
#include <SFE_LSM9DS0.h>
#define LSM9DS0_XM  0x1D
#define LSM9DS0_G   0x6B
LSM9DS0 dof(MODE_I2C, LSM9DS0_G, LSM9DS0_XM);
float gx, gy, gz, pitch, roll, ax, ay, az, mx, my, mz, heading;

// Stuff for GPS
#include <TinyGPS.h>
TinyGPS gps;
float lat, lon, alt, mps, gps_heading;
unsigned long chars, fix_age, time, date;
unsigned short sentences, failed;

// Stuff for MPU6050
#include "I2Cdev.h"
#include "MPU6050.h"
#define MPU6050_PWR_MGMT_1    0x6B 
#define MPU6050_I2C_ADDRESS   0x68
MPU6050 accelgyro;
int16_t aax, aay, aaz, agx, agy, agz, aroll, apitch;
const float pi = 3.14159265;
const float alpha = 0.5;
uint8_t c = 0;
double fXg = 0;
double fYg = 0;
double fZg = 0;

// ADC
#include <Adafruit_ADS1015.h>
Adafruit_ADS1115 ads;
int adc0, adc1;
float vout, isense;


//for sending data
float gx_data, gy_data, gz_data, pitch_data, roll_data, ax_data, ay_data, az_data, heading_data;
float lat_data, lon_data, alt_data, mps_data, gps_heading_data, time_data, date_data;
float aroll_data, apitch_data; 
float vout_data, isense_data;

int iter = 0; 


void setup() {
  // Begin the LSM9DS0
  dof.begin();
  
  // Begin the GPS and comms
  Serial1.begin(9600);
  
  // Begin the MPU6050
  Wire.begin();
  MPU6050_write(MPU6050_PWR_MGMT_1, &c, 1); //Stop device from reseting/sleeping
  accelgyro.initialize();
  
  // Begin the ADC
  ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 3mV      0.1875mV
  ads.begin();
  
  // For testing
  Serial.begin(115200);
  
}

void loop() {
  
  // LSM9DS0
  dof.readGyro();
  gx = dof.calcGyro(dof.gx);
  gy = dof.calcGyro(dof.gy);
  gz = dof.calcGyro(dof.gz);
  pitch = getPitch(gx, gy, gz);
  roll = getRoll(gx, gy, gz);
  
  dof.readAccel();
  ax = dof.calcAccel(dof.ax);
  ay = dof.calcAccel(dof.ay);
  az = dof.calcAccel(dof.az);
  
  dof.readMag();
  mx = dof.calcMag(dof.mx);
  my = dof.calcMag(dof.my);
  mz = dof.calcMag(dof.mz);
  heading = getHeading(mx, my);
  
  // GPS
  while(Serial1.available()){
    int c = Serial1.read();
    if(gps.encode(c)){
      gps.f_get_position(&lat, &lon, &fix_age);
      mps = gps.f_speed_mps();
      alt = gps.f_altitude();
      gps_heading = gps.f_course();
      gps.get_datetime(&date, &time, &fix_age);
      gps.stats(&chars, &sentences, &failed);
    }
  }
  
  // MPU6050
  accelgyro.getMotion6(&aax, &aay, &aaz, &agx, &agy, &agz);
  //Low Pass Filter
  fXg = agx * alpha + (fXg * (1.0 - alpha));
  fYg = agy * alpha + (fYg * (1.0 - alpha));
  fZg = agz * alpha + (fZg * (1.0 - alpha));
  aroll  = ((atan2(-fYg, fZg)*180.0)/pi );
  apitch = ((atan2(fXg, sqrt(fYg*fYg + fZg*fZg))*180.0)/pi);
  
  // ADC
  
  adc0 = ads.readADC_SingleEnded(0);
  adc1 = ads.readADC_SingleEnded(1);
  vout = 0.000778547*adc1-0.0866782;
  isense = adc0;
  
  //Serial.println(vout);
  //Serial.println(isense); 
  
  // collects average of data over 10 iterations
  if(iter == 0){
    pitch_data = pitch;
    roll_data = roll;
    gx_data = gx;
    gy_data = gy;
    gz_data = gz;
    ax_data = ax;
    ay_data = ay; 
    az_data = az;
    heading_data = heading;
    aroll_data = aroll;
    apitch_data = apitch;
    lat_data = lat;
    lon_data = lon;
    mps_data = mps;
    alt_data = alt;
    gps_heading_data = gps_heading;
    date_data = date;
    time_data = time; 
    vout_data = vout; 
    isense_data = isense;
    
    iter =+ 1; 
  } 
  else if(iter == 10) {
    // print all data : pitch roll gx gy gz ax ay az heading aroll apitch lat lon mps alt gps_heading date time vout isense
    Serial.print("#");
    Serial.print(pitch_data / 10); //0
    Serial.print(" ");
    Serial.print(roll_data / 10); //1
    Serial.print(" ");
    Serial.print(gx_data / 10);  //2
    Serial.print(" ");
    Serial.print(gy_data / 10);  //3
    Serial.print(" ");
    Serial.print(gz_data / 10);  //4
    Serial.print(" ");
    Serial.print(ax_data / 10);  //5
    Serial.print(" ");
    Serial.print(ay_data / 10);  //6
    Serial.print(" ");
    Serial.print(az_data / 10);  //7
    Serial.print(" ");
    Serial.print(heading_data / 10);  //8
    Serial.print(" ");
    Serial.print(aroll_data / 10);  //9
    Serial.print(" ");
    Serial.print(apitch_data / 10);  //10
    Serial.print(" ");
    Serial.print(lat_data / 10,8);  //11
    Serial.print(" ");
    Serial.print(lon_data / 10,8);  //12
    Serial.print(" ");
    Serial.print(mps_data / 10);  //13
    Serial.print(" ");
    Serial.print(alt_data / 10);  //14
    Serial.print(" ");
    Serial.print(gps_heading_data / 10);   //15
    Serial.print(" ");
    Serial.print(date_data / 10);  //16
    Serial.print(" ");
    Serial.print(time_data / 10);  //17
    Serial.print(" ");
    Serial.print(vout_data / 10);  //18
    Serial.print(" ");
    Serial.print(isense_data / 10);  //19
    Serial.print(" ");
    Serial.print(checksum(roll_data / 10,time_data / 10,heading_data / 10));
    Serial.println("$");
  
    iter = 0;
  }
  else{
    pitch_data += pitch;
    roll_data += roll;
    gx_data += gx;
    gy_data += gy;
    gz_data += gz;
    ax_data += ax;
    ay_data += ay; 
    az_data += az;
    heading_data += heading;
    aroll_data += aroll;
    apitch_data += apitch;
    lat_data += lat;
    lon_data += lon;
    mps_data += mps;
    alt_data += alt;
    gps_heading_data += gps_heading;
    date_data += date;
    time_data += time; 
    vout_data += vout; 
    isense_data += isense;
    
    iter += 1; 
  } 
}

int checksum(float a, float b, float c){
  int sum = a * b * c;
  return sum%256;
}

// Calculates earth's magnetic heading if sensor is flat
// Need to add or subtract a declination for Utah
float getHeading(float hx, float hy)
{
  float heading;
  float dec = 10.65; // Saskatoon
  // float dec = 10.90; // utah 
  
  if (hy > 0){
    heading = 90 -  (atan(hx / hy) * (180 / PI));
  }
  else if (hy < 0){
    heading = 270 - (atan(hx / hy) * (180 / PI));
  }
  else{ // hy = 0
    if (hx < 0) heading = 180;
    else heading = 0;
  }
  // declination for Saskatoon
  heading = heading + dec;
  
  if (heading >= 360) {
    heading = heading - 360;   
  }
  return heading;
}

// Gets pitch in degrees
float getPitch(float x, float y, float z){
  float pitch;
  pitch = atan2(x, sqrt(y * y) + (z * z));
  pitch *= 180.0 / PI;
  return pitch;
}

// Gets roll in degrees
float getRoll(float x, float y, float z){
  float roll;
  roll = atan2(y, sqrt(x * x) + (z * z));
  roll *= 180.0 / PI;
  return roll;
}

// Manages MPU6050 commands
int MPU6050_write(int address, uint8_t *data, int size) {
  Wire.beginTransmission(MPU6050_I2C_ADDRESS);
  Wire.write(address);        // write the start address
  Wire.write(data, size);  // write data bytes
  Wire.endTransmission(true); // release the I2C-bus
  return (0);         // return : no error
}
