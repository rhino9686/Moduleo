
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266mDNS.h>
#include <ArduinoOTA.h>
#include <ESP8266WebServer.h>
#include <ESP8266WiFiMulti.h> 
#include <ESP8266HTTPClient.h>

enum example {
  unknown,
  true,
  false
};


// If in setup mode, this will be true and chip will broadcast it's own network for setup
bool SETUP_MODE = false;


//HTTPClient to send messages to server
HTTPClient http;

//IP Addresses for Access Point Mode
IPAddress ip(192,168,11,4);
IPAddress gateway(192,168,11,1);
IPAddress subnet(255,255,255,0);


// Server handler declarations
// should be agnostic between HTTP and Socket implementations

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



void setup() {
  // put your setup code here, to run once:

  
}

void loop() {
  // put your main code here, to run repeatedly:

}


//// SETUP MODE ///////////////////////////////////////////////////////////

// this will switch to Setup mode
void switchToSetupMode() {
  SETUP_MODE = true;

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

  return;
}
