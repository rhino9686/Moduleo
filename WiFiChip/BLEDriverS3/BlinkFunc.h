/*
  BLEDriverS3.ino

  SIMPLIFIED VERSION.

  Everything lives in this one file now:
    - Bluepad32 connects to the Xbox controller
    - One function, ledBlink(), looks at the controller and decides what
      the LED should do
    - loop() just calls BP32.update() and then ledBlink() every cycle

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

// --- Globals -----------------------------------------------------------

// Bluepad32 can track up to 4 controllers at once (BP32_MAX_GAMEPADS).
// We only care about ONE controller for this simple version, so we just
// keep a single pointer. It starts out "null" (no controller connected).
ControllerPtr myController = nullptr;

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
  myController = ctl;
}

void onDisconnectedController(ControllerPtr ctl) {
  // A controller disconnected. If it's the one we were tracking, forget it.
  if (myController == ctl) {
    Serial.println("Controller disconnected!");
    myController = nullptr;
  }
}

// --- The one LED function ------------------------------------------------
//
// This is the whole "brain" of the debug behavior. It looks at the
// controller's current state and decides what the LED should do:
//
//   1) If ANY face button (A/B/X/Y) is held down       -> LED solid ON
//   2) Else if a stick is pushed past the deadzone      -> LED blinks
//      (faster blink the further you push the stick)
//   3) Otherwise (idle, or no controller connected)     -> LED OFF
//
// Change the logic in here freely — it's the only place you need to edit
// to change what the LED does in response to input.

void ledBlink() {
  // --- No controller connected: LED off, nothing else to do ---
  if (myController == nullptr || !myController->isConnected()) {
    digitalWrite(LED_PIN, LOW);
    ledIsOn = false;
    return;
  }

  // --- Read the buttons we care about ---
  // Bluepad32 gives you one function per button, returning true/false.
  bool anyFaceButtonPressed =
      myController->a() || myController->b() ||
      myController->x() || myController->y();

  // --- Case 1: face button held -> solid LED, skip blinking entirely ---
  if (anyFaceButtonPressed) {
    digitalWrite(LED_PIN, HIGH);
    ledIsOn = true;

    Serial.println("Event captured");
    return;  // done for this loop() call
  }

  // --- Read the sticks ---
  // Bluepad32 reports stick position as roughly -512 to +512 (raw units).
  // We divide by 512.0 to convert that into a friendlier -1.0 to +1.0 range.
  float leftStickX = myController->axisX() / 512.0f;
  float leftStickY = myController->axisY() / 512.0f;
  float rightStickX = myController->axisRX() / 512.0f;
  float rightStickY = myController->axisRY() / 512.0f;

  // Combine X and Y into one "how far is the stick pushed, in any
  // direction" number using the Pythagorean theorem (distance formula).
  // We do this for both sticks and just use whichever is pushed further.
  float leftStickMagnitude = sqrtf(leftStickX * leftStickX + leftStickY * leftStickY);
  float rightStickMagnitude = sqrtf(rightStickX * rightStickX + rightStickY * rightStickY);
  float stickMagnitude = max(leftStickMagnitude, rightStickMagnitude);

  // --- Case 2: a stick is pushed past the deadzone -> blink ---
  if (stickMagnitude > STICK_DEADZONE) {
    // Map how far the stick is pushed (deadzone..1.0) to a blink speed
    // (slow blink when barely past the deadzone, fast blink when maxed out).
    //
    // "t" below is a 0.0-to-1.0 progress value: 0 = just past the
    // deadzone, 1 = stick pushed all the way to the edge.
    float t = (stickMagnitude - STICK_DEADZONE) / (1.0f - STICK_DEADZONE);
    t = constrain(t, 0.0f, 1.0f);

    // Blink interval: 300ms (slow) when t=0, down to 60ms (fast) when t=1.
    unsigned long blinkIntervalMs = (unsigned long)(300 - t * (300 - 60));

    // Non-blocking blink: only toggle the LED if enough time has passed
    // since the last toggle. This is the "blink without delay()" trick.
    unsigned long now = millis();
    if (now - lastBlinkToggleTime >= blinkIntervalMs) {
      lastBlinkToggleTime = now;
      ledIsOn = !ledIsOn;  // flip the LED state
      digitalWrite(LED_PIN, ledIsOn ? HIGH : LOW);
    }
    return;  // done for this loop() call
  }

  // --- Case 3: idle (no button, no stick movement) -> LED off ---
  digitalWrite(LED_PIN, LOW);
  ledIsOn = false;
}

// --- Standard Arduino setup/loop -----------------------------------------

void setupExample() {
  Serial.begin(115200);
  delay(500);  // give the Serial Monitor a moment to connect

  Serial.println("Starting up...");

  // Set up the LED pin as an output so we can turn it on/off.
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);  // start with it off

  // This line is REQUIRED. It tells Bluepad32 which functions to call
  // when a controller connects or disconnects (the two functions defined
  // above), and starts the Bluetooth scanning process in the background.
  BP32.setup(&onConnectedController, &onDisconnectedController);

  Serial.println("Ready. Turn on your Xbox controller and hold its Pair");
  Serial.println("button (near the top, next to the USB-C port) for ~3 seconds.");
}

void loopExample() {
  // MUST be called every loop iteration. This is what actually checks
  // for new Bluetooth data and updates myController's button/stick values
  // behind the scenes.
  BP32.update();

  // Now that the controller data (if any) is fresh, decide what the LED
  // should do this cycle.
  ledBlink();
  delay(200);
  // No delay() here on purpose — ledBlink() is non-blocking, and BP32.update()
  // needs to be called as often as possible to stay responsive.
}
