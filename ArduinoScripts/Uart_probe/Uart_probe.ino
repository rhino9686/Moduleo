char datumRec = 'G';

char datumSend = 'H';

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:

  delay(1000);

/**  if (Serial.available()){
      datumRec = Serial.read();
      Serial.write(datumSend);
  }
**/
  datumSend = 'H';
  Serial.write(datumSend);
  delay(1000);
  
  datumSend = "F";
  Serial.write(datumSend);
  delay(1000);
  
  datumSend = "L";
  Serial.write(datumSend);
  delay(1000);
  
  datumSend = "R";
  Serial.write(datumSend);
  delay(1000);
}
