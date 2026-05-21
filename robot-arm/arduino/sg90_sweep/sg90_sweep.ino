#include <Servo.h>

// SG90 signal wire (orange/yellow) -> Arduino digital pin 9
// SG90 red -> external +5V (or Arduino 5V for no-load quick test only)
// SG90 brown/black -> GND
// IMPORTANT: Arduino GND and servo power GND must be connected together.

Servo elbow;
const int SERVO_PIN = 9;

void setup() {
  elbow.attach(SERVO_PIN);
  elbow.write(90);   // center first
  delay(1000);
}

void loop() {
  elbow.write(20);   // avoid hard endpoints at first
  delay(1000);
  elbow.write(90);
  delay(1000);
  elbow.write(160);
  delay(1000);
  elbow.write(90);
  delay(1000);
}
