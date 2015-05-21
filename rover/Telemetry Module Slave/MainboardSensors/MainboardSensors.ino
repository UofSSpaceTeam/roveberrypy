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
Adafruit_ADS1115 adc(0x48);
Adafruit_ADS1015 adcExp(0x49);


float lat, lon, alt, mps, heading;
unsigned long fix_age, time, date;
float gx, gy, gz, ax, ay, az, mx, my, mz, vout, isense, laser, ph, moist;
float gx_avg, gy_avg, gz_avg, ax_avg, ay_avg, az_avg;
float mx_avg, my_avg, mz_avg, vout_avg, isense_avg, laser_avg, ph_avg, moist_avg;

int count = 0;
const int ledPin = 13;

void setup()
{
        delay(1000)
	Serial1.begin(9600); // GPS + pi
	pinMode(ledPin, OUTPUT);
	resetAverages();
	
	Wire.begin();
	imu.begin();
	
	adc.setGain(GAIN_TWOTHIRDS); // 2/3x gain +/- 6.144V 1 bit = 3mV 0.1875mV
	adc.begin();

        adcExp.setGain(GAIN_ONE);
        adcExp.begin();

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

        adcExp.setGain(GAIN_ONE);
        laser = adcExp.readADC_SingleEnded(0);
        adcExp.setGain(GAIN_FOUR);
        ph = adcExp.readADC_SingleEnded(1);
        moist = adcExp.readADC_SingleEnded(2);
	
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
	Serial1.print(gx_avg / 10); // 1
	Serial1.print(" ");
	Serial1.print(gy_avg / 10); // 2
	Serial1.print(" ");
	Serial1.print(gz_avg / 10); // 3
	Serial1.print(" ");
	Serial1.print(ax_avg / 10); // 4
	Serial1.print(" ");
	Serial1.print(ay_avg / 10); // 5
	Serial1.print(" ");
	Serial1.print(az_avg / 10); // 6
	Serial1.print(" ");
	Serial1.print(mx_avg / 10); // 7
	Serial1.print(" ");
	Serial1.print(my_avg / 10); // 8
	Serial1.print(" ");
	Serial1.print(mz_avg / 10); // 9
	Serial1.print(" ");
	Serial1.print(lat, 8); // 10
	Serial1.print(" ");
	Serial1.print(lon, 8); // 11
	Serial1.print(" ");
	Serial1.print(mps); // 12
	Serial1.print(" ");
	Serial1.print(alt); // 13
	Serial1.print(" ");
	Serial1.print(heading); // 14
	Serial1.print(" ");
	Serial1.print(date); // 15
	Serial1.print(" ");
	Serial1.print(time); // 16
	Serial1.print(" ");
	Serial1.print(vout_avg); // 17
	Serial1.print(" ");
	Serial1.print(isense_avg); // 18
        Serial1.print(" ");
        Serial1.print(laser_avg); // 19
	Serial1.print(" ");
	Serial1.print(ph_avg); // 20
        Serial1.print(" ");
        Serial1.print(moist_avg); //21
        Serial1.println("$");
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
        laser_avg += laser;
        ph_avg += ph;
        moist_avg += moist;
        
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
        laser_avg = 0;
        ph_avg = 0;
        moist_avg = 0;
}

