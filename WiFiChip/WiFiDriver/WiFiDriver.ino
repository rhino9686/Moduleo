
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266mDNS.h>
#include <ArduinoOTA.h>
#include <ESP8266WebServer.h>
#include <ESP8266WiFiMulti.h> 
#include <ESP8266HTTPClient.h>

enum example {
  exval1,
  exval2,
  exval3
};

struct AirParams {
  int val1;
  int val2;
  int val3;
};

// If in setup mode, this will be true and chip will broadcast it's own network for setup
bool SETUP_MODE = false;


const char* ssidFiller = "MSetup";
//ssid and password for Access Point
const char* ssid = "FishTank";  //Previously MadiWifi, duly noted
const char* password = "password";

const char* myIP = "192,168,11,4";


// HTTPClient to send messages to server
HTTPClient http;

// IP Addresses for Access Point Mode
IPAddress ip(192,168,11,4);
IPAddress gateway(192,168,11,1);
IPAddress subnet(255,255,255,0);

// Server object
ESP8266WebServer server(80);

char buf[4];



// Server handler declarations
// should be agnostic between HTTP and Socket implementations

// sends a char over UART to the main board
// dependency for the declarations below
// returns 0 for success, -1 for error (for optional logging)
int sendMessage(char msg);

// sends message over UART for drone to go forward for a unit of time
void goForward();

// sends message over UART for drone to continuously move forward
void continuousForward();

// sends message over UART for drone to go backward for a unit of time
void goBackward();

// sends message over UART for drone to continuously move backward
void continuousBackward();

// sends message over UART for drone to rotate left for a unit of time
void turnLeft();

// sends message over UART for drone to rotate right for a unit of time
void turnRight();

// sends message over UART to request an air sample
void requestAirStatus(char param);

// Switches to broadcasting it's own Wi-Fi network
void switchToSetupMode();

// Switches to connecting to a new network
void switchToOperationalMode();



void setup() {
  Serial.begin(9600);
  Serial.println("starting up!");

  switchToSetupMode();

    //Handler for http requests for requests
    server.on("/goForward", goForward);
}

void loop() {
 

  //Serial.println("Hi");

}


//// SETUP MODE ///////////////////////////////////////////////////////////

// this will switch to Setup mode
void switchToSetupMode() {

  // toggle our own variable 
  SETUP_MODE = true;

  // switch to WIFI_AP_STA mode where this chip broadcasts its own network
  WiFi.mode(WIFI_AP_STA);
  
  Serial.println(WiFi.softAPConfig(ip, gateway, subnet) ? "Ready" : "Failed!");
  Serial.print(" Setting softAP " );
  Serial.println(WiFi.softAP(ssid, password) ? "Ready" : "Failed!");

  
  return;
}

void switchToOperationalMode() {
  SETUP_MODE = false;
  WiFi.softAPdisconnect(true);
  WiFi.mode(WIFI_STA);


  WiFi.begin(ssid, password);
  
  if (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("WiFi Connect Failed! Rebooting...");
    delay(1000);
    ESP.restart();
  }

  return;
}
//// END SETUP MODE ////////////////////////////////////////////////////////




int sendMessage(char msg){
    Serial.write(msg);
    //can swap out with softwareSerial here

    return 0;
}

// sends message over UART for drone to go forward for a unit of time
void goForward() {
  sendMessage('F');
}

// sends message over UART for drone to continuously move forward
void continuousForward() {
  sendMessage('f');
}

// sends message over UART for drone to go backward for a unit of time
void goBackward() {
  sendMessage('B');
}

// sends message over UART for drone to continuously move backward
void continuousBackward(){
  sendMessage('b');
}

// sends message over UART for drone to rotate left for a unit of time
void turnLeft() {
  sendMessage('L');
}

// sends message over UART for drone to rotate right for a unit of time
void turnRight() {
  sendMessage('R');
}
