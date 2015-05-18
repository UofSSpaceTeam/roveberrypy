#include <Wire.h>
#include <I2Cdev.h>
#include <SPI.h>
#include <SFE_LSM9DS0.h>
#include <TinyGPS.h>
#include <Adafruit_ADS1015.h>

#define LSM9DS0_XM 0x1D
#define LSM9DS0_G 0x6B
#define ITERATIONS 25

LSM9DS0 imu(MODE_I2C, LSM9DS0_G, LSM9DS0_XM);
TinyGPS gps;
Adafruit_ADS1115 adc;

float lat, lon, alt, mps, heading;
unsigned long fix_age, time, date;
float gx, gy, gz, ax, ay, az, mx, my, mz, vout, isense;
float gx_avg, gy_avg, gz_avg, ax_avg, ay_avg, az_avg;
float mx_avg, my_avg, mz_avg, vout_avg, isense_avg;

int count = 0;
const int ledPin = 13;

void setup()
{
	Serial1.begin(9600); // GPS
	Serial.begin(57600); // pi
	pinMode(ledPin, OUTPUT);
	resetAverages();
	
	Wire.begin();
	imu.begin();
	
	adc.setGain(GAIN_TWOTHIRDS); // 2/3x gain +/- 6.144V 1 bit = 3mV 0.1875mV
	adc.begin();
}

void loop()
{
	delay(5);
	imu.readGyro();
	gx = imu.calcGyro(imu.gx);
	gy = imu.calcGyro(imu.gy);
	gz = imu.calcGyro(imu.gz);
	imu.readAccel();
	ax = imu.calcAccel(imu.ax);
	ay = imu.calcAccel(imu.ay);
	az = imu.calcAccel(imu.az);
	imu.readMag();
	mx = imu.calcMag(imu.mx);
	my = imu.calcMag(imu.my);
	mz = imu.calcMag(imu.mz);
	
	while(Serial1.available())
	{
		if(gps.encode(Serial1.read()))
		{
			gps.f_get_position(&lat, &lon, &fix_age);
			mps = gps.f_speed_mps();
			alt = gps.f_altitude();
			heading = gps.f_course();
			gps.get_datetime(&date, &time, &fix_age);
		}
	}

	isense = adc.readADC_SingleEnded(0);
	vout = adc.readADC_SingleEnded(1);
	vout = (vout * 0.000778547) - 0.0866782;
	
	// collects average of data over 10 iterations
	if(count < ITERATIONS)
	{
		addToAverages();
		count++;
	}
	else
	{
		count = 0;
		digitalWrite(ledPin, HIGH);	
		sendData();
		digitalWrite(ledPin, LOW);
		resetAverages();
	}
}

void sendData()
{
	Serial.print("#");
	Serial.print(gx_avg / 10); // 1
	Serial.print(" ");
	Serial.print(gy_avg / 10); // 2
	Serial.print(" ");
	Serial.print(gz_avg / 10); // 3
	Serial.print(" ");
	Serial.print(ax_avg / 10); // 4
	Serial.print(" ");
	Serial.print(ay_avg / 10); // 5
	Serial.print(" ");
	Serial.print(az_avg / 10); // 6
	Serial.print(" ");
	Serial.print(mx_avg / 10); // 7
	Serial.print(" ");
	Serial.print(my_avg / 10); // 8
	Serial.print(" ");
	Serial.print(mz_avg / 10); // 9
	Serial.print(" ");
	Serial.print(lat, 8); // 10
	Serial.print(" ");
	Serial.print(lon, 8); // 11
	Serial.print(" ");
	Serial.print(mps); // 12
	Serial.print(" ");
	Serial.print(alt); // 13
	Serial.print(" ");
	Serial.print(heading); // 14
	Serial.print(" ");
	Serial.print(date); // 15
	Serial.print(" ");
	Serial.print(time); // 16
	Serial.print(" ");
	Serial.print(vout); // 17
	Serial.print(" ");
	Serial.print(isense); // 18
	Serial.println("$");
}

void addToAverages()
{
	gx_avg += gx;
	gy_avg += gy;
	gz_avg += gz;
	ax_avg += ax;
	ay_avg += ay; 
	az_avg += az;
	mx_avg += mx;
	my_avg += my; 
	mz_avg += mz;
	vout_avg += vout;
	isense_avg += isense;
}

void resetAverages()
{
	gx_avg = 0;
	gy_avg = 0;
	gz_avg = 0;
	ax_avg = 0;
	ay_avg = 0;
	az_avg = 0;
	mx_avg = 0;
	my_avg = 0;
	mz_avg = 0;
	vout_avg = 0;
	isense_avg = 0;
}

