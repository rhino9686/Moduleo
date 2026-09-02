/*
  BLEDriverS3.ino

  Board package required: "esp32_bluepad32" (NOT the plain "esp32" board
  package — Bluepad32 needs its own board definitions because it replaces
  the default Bluetooth stack).
*/

#include <Bluepad32.h>  // Gives us the ControllerPtr type and BP32 object

// --- Configuration ---------------------------------------------------

#define LED_PIN 4  // Which GPIO the debug LED is wired to

// How far you have to push a stick before we count it as "moved".
// Sticks rest at 0 but almost never read EXACTLY 0 due to hardware
// tolerance, so without a deadzone the LED would blink even at rest.
#define STICK_DEADZONE 0.15f


struct Button{

  bool pressedLastCycle = 0;

  bool isPressed(bool isPressedNow){

    bool edge = (isPressedNow && !pressedLastCycle);
    pressedLastCycle = isPressedNow;
    return edge;
  }

};

bool setupButton(Button*);



enum Direction {

  LEFT,
  RIGHT,
  UP,
  DOWN

};

struct Joystick {

  ControllerPtr ctl;
  bool leftStick;

  float readX(){
    if (leftStick){
      return (ctl->axisX())/512.0f;
    }
    else return (ctl->axisRX())/512.0f;
  }

  float readY(){
    if (leftStick){
      return (ctl->axisY())/512.0f;
    }
    else return (ctl->axisRY())/512.0f;
  }

  Direction getDirection(){
    
  }

};

bool setupJoystick(Joystick*, ControllerPtr ctl, bool leftStick);


// --- Globals -----------------------------------------------------------

// Bluepad32 can track up to 4 controllers at once (BP32_MAX_GAMEPADS).
// We only care about ONE controller for this simple version, so we just
// keep a single pointer. It starts out "null" (no controller connected).
ControllerPtr myController = nullptr;

Button A;
Button B;
Button X;
Button Y;

Joystick leftJ;
Joystick rightJ;

// These track LED blinking state between loop() calls, so the LED can
// blink without ever calling delay() (which would freeze the whole
// program, including the Bluetooth polling, while it waited).
bool ledIsOn = false;
unsigned long lastBlinkToggleTime = 0;

// --- Bluepad32 callbacks ------------------------------------------------
// These two functions are called AUTOMATICALLY by the Bluepad32 library
// whenever a controller connects or disconnects. You never call them
// yourself — you just hand their names to BP32.setup() below, and the
// library calls them for you when the event happens.

void onConnectedController(ControllerPtr ctl) {
  // A controller connected. Since we're only tracking one, just grab it.
  Serial.println("Controller connected!");

  digitalWrite(LED_PIN, HIGH);  
  myController = ctl;
}

void onDisconnectedController(ControllerPtr ctl) {
  // A controller disconnected. If it's the one we were tracking, forget it.
  if (myController == ctl) {
    Serial.println("Controller disconnected!");
    myController = nullptr;
  }
}


void setup() {
  Serial.begin(115200);
  delay(500);  // give the Serial Monitor a moment to connect

  Serial.println("Starting up...");

  // Set up the LED pin as an output so we can turn it on/off.
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);  // start with it off

  // Setting up the attached functions for onConnection and onDisconnect
  BP32.setup(&onConnectedController, &onDisconnectedController);

  setupJoystick(&leftJ, myController, true);
  setupJoystick(&rightJ, myController, false);


  Serial.println("Ready. Turn on your Xbox controller and hold its Pair");
  Serial.println("button (near the top, next to the USB-C port) for ~3 seconds.");
}

void loop() {
  // MUST be called every loop iteration. This is what actually checks
  // for new Bluetooth data and updates myController's button/stick values
  // behind the scenes.
  BP32.update();
  // needs to be called as often as possible to stay responsive.

}

bool setupButton(Button* btn){

}

bool setupJoystick(Joystick* joy, ControllerPtr ctl, bool leftStick){

  joy->leftStick = leftStick;
  joy->ctl = ctl;

}



