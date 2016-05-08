#include "moc.h"

uint_t dir = 0;



///////////////////////////////////////////////////////////////////////////////
//          Motor Controllers
///////////////////////////////////////////////////////////////////////////////

const MOC_SPEC moc_spec[] = {
    {0, 20, INTERNAL_FB, INVALID_U, 15, 0},
    {1, 21, INTERNAL_FB, INVALID_U, 15, 0},
    {2, 22, INTERNAL_FB, INVALID_U, 15, 0},
    {3, 23, INTERNAL_FB, INVALID_U, 15, 0},
    {4, 5,  INTERNAL_FB, INVALID_U, 15, 0},
    {5, 6,  INTERNAL_FB, INVALID_U, 15, 0},
    {6, 9,  INTERNAL_FB, INVALID_U, 15, 0},
    {7, 10, INTERNAL_FB, INVALID_U, 15, 0}
};

void moc_initializePins() {
     pinMode(_MOCHI_SEL[0],     OUTPUT);
     pinMode(_MOCHI_SEL[1],     OUTPUT);
     pinMode(_MOCHI_SEL[2],     OUTPUT);
     pinMode(_MOCHI_DAT,        OUTPUT);
     pinMode(_MOCHI_WRT,        OUTPUT);
     pinMode(_MOCHI_CSEL[0],    OUTPUT);
     pinMode(_MOCHI_CSEL[1],    OUTPUT);
     pinMode(_MOCHI_CSEL[2],    OUTPUT);
     pinMode(_MOCHI_CSEL[3],    OUTPUT);
     pinMode(_MOCHI_CRD,        INPUT);
     pinMode(_MOCHI_CRST,       OUTPUT);
     for(uint_t i = 0; i < 8; ++i) {
         //pinMode(moc_spec[i].PIN_PWM, OUTPUT);
         //moc_setSpeed(moc_spec + i, 0);
         if (moc_spec[i].EXT_FB) {
            //pinMode(moc_spec[i].PIN_EXT_FB, INPUT);
        }
     }
}

void setup() {
  delay(2000);
  Serial.begin(9600);
  Serial.println("Init pins");
  moc_initializePins();
}

void loop() {
  
  moc_setDirection(moc_spec + 3, 1);
  analogWrite(23, 255);
  delay(5000);
  //digitalWrite(13, 1);
  moc_setDirection(moc_spec + 3, 0);
  analogWrite(23, 0);
  delay(5000);
  //digitalWrite(13, 0);
  
}
