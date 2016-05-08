//////////////////////////////////////////////////////////////////////
// PINS: 2,3
// Baud: 115200
// Test code for Adafruit GPS modules using MTK3329/MTK3339 driver
//    ------> http://www.adafruit.com/products/746
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>
SoftwareSerial mySerial(3, 2);
Adafruit_GPS GPS(&mySerial);
#define GPSECHO  true
boolean usingInterrupt = false;
void useInterrupt(boolean); // Func prototype keeps Arduino 0023 happy
void GPS_setup()  
{
  //Serial.begin(115200);
  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate
  GPS.sendCommand(PGCMD_ANTENNA);
  useInterrupt(true);
  delay(1000);
}
SIGNAL(TIMER0_COMPA_vect) {
  char c = GPS.read();
}
void useInterrupt(boolean v) {
  if (v) {
    OCR0A = 0xAF;
    TIMSK0 |= _BV(OCIE0A);
    usingInterrupt = true;
  } else {
    TIMSK0 &= ~_BV(OCIE0A);
    usingInterrupt = false;
  }
}
uint32_t timer = millis();
void GPS_loop()
{
  if (timer > millis())  timer = millis();
  if (millis() - timer > 1000) { 
    timer = millis();
    if (1) {
      Serial.print("('GPS',");
      Serial.print(GPS.latitudeDegrees, 4);
      Serial.print(", "); 
      Serial.print(GPS.longitudeDegrees, 4);
      Serial.print(",");
      Serial.print(GPS.speed);
      Serial.println(")");
    }
  }
}
//
////////////////////////////////////////////////////////////////////////



