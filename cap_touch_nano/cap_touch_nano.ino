#include <CapacitiveSensor.h>
#include "Statistic.h"

Statistic data;
CapacitiveSensor cs_4_2 = CapacitiveSensor(12, 11);  // 10 megohm resistor between pins 4 & 2, pin 2 is sensor pin, add wire, foil
const int LEDpin = 2;
int motorPin = 3; //motor transistor is connected to pin 3
int motorPin2 = 2; //motor transistor is connected to pin 3

// int speed = 127; // speed of the motor (0-255):
float lastDev = 0;        // previous standard deviation

void setup(void) {
  data.clear();  // explicitly start clean

  pinMode(LEDpin, OUTPUT);
  digitalWrite(LEDpin, LOW);

  // set all the other pins you're using as outputs:
  pinMode(motorPin, OUTPUT);
  pinMode(motorPin2, OUTPUT);

  // set capacitive sensor timing
  cs_4_2.set_CS_AutocaL_Millis(0xFFFFFFFF);  // turn off autocalibrate on channel 1 - 
}

void loop(void) {
  long start = millis();
  long total = cs_4_2.capacitiveSensor(30);
  data.add(total);

  float currentDev = data.pop_stdev();
  Serial.println(currentDev);

  if (currentDev >= lastDev) { // if touched, run motor
    digitalWrite(motorPin, HIGH); //vibrate
    digitalWrite(motorPin2, HIGH); //vibrate
    // Serial.println("on");
    digitalWrite(LEDpin, HIGH);
  } else { // else turn motor off
    // Serial.println("off");
    digitalWrite(motorPin, LOW);  //stop vibrating
    digitalWrite(motorPin2, LOW);  //stop vibrating
    digitalWrite(LEDpin, LOW);
  }

  lastDev = currentDev;
  delay(10);  // arbitrary delay to limit data to serial port
}