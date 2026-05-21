#include <Servo.h>

Servo elbow;
const int SERVO_PIN = 9;

void setup() {
  elbow.attach(SERVO_PIN);
  elbow.write(90);      // move/hold center briefly
  delay(300);
  elbow.detach();       // stop sending servo pulses
}

void loop() {
  // do nothing
}
