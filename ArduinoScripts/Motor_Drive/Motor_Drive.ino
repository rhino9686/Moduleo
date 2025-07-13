int pinF = 3;

int pinB = 5;

int pinFLevel;

int pinBLevel;

int direction = 0;


void setup() {
  // put your setup code here, to run once:

  direction = 0;

  Serial.begin(9600);

  pinMode(pinF, OUTPUT);
  pinMode(pinB, OUTPUT); 

  setPin(pinF, 0);
  setPin(pinB, 0);

  pinFLevel = 0;
  pinBLevel = 0;

}

void loop() {
  // put your main code here, to run repeatedly:

  delay(1000);

  pinFLevel = 50;

  setPin(pinF, pinFLevel);


  delay(1000);
}
