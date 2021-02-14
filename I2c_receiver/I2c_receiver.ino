#include "Wire.h"


void response();

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin(0x81);

  Wire.onRequest(response);

}

void loop() {
  // put your main code here, to run repeatedly:

}

 //handler for receiving request on I2C line 
void response() {

  Serial.print("beep");
}
