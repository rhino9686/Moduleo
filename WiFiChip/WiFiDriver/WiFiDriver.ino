
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266mDNS.h>
#include <ArduinoOTA.h>
#include <ESP8266WebServer.h>
#include <ESP8266WiFiMulti.h> 
#include <ESP8266HTTPClient.h>
#include "privates.h"

//Character definition constants


#define DEBUG_MODE 0      //  flag for optional Debug stuff

#define FORWARD 'F'       //  To send message over UART for drone to go forward for a unit of time
#define FORWARD_CONT 'f'  //  To send message over UART for drone to continuously move forward
#define BACKWARD 'B'      //  To send message over UART for drone to go backward for a unit of time
#define BACKWARD_CONT 'b' //  To send message over UART for drone to continuously move backwards
#define LEFT 'L'          //  To send message over UART for drone to rotate left for a unit of time
#define RIGHT 'R'         //  To send message over UART for drone to rotate right for a unit of time
#define HALT 'H'          //  To send message over UART for drone to halt


char cmdSelected = 'A';

// placeholder enum
enum example {
  exval1,
  exval2,
  exval3
};


// placeholder struct
struct AirParams {
  int val1;
  int val2;
  int val3;
};

// If in setup mode, this will be true and chip will broadcast it's own network for setup
bool SETUP_MODE = false;


//ssid and password for our own Access Point
const char* ssid = "groundControl";  
const char* password = "password";

//ssid and password for connecting to someone else's
const char* ssidCentral = "ATT4PrY5GD";
const char* passwordCentral = PASSWORD;  //found in privates.h which is not stored in git

const char* myIP = "192,168,11,4"; // My own set IP Addr


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

int sendMessage(String msg);


// Tester helper
void handleRoot();

//function that can split off into any of the remaining funcs depending on what args are sent with it
void handleCommand();

// sends message over UART to request an air sample
void requestSensorStatus(char param);

// Switches to broadcasting it's own Wi-Fi network
void switchToSetupMode();

// Switches to connecting to a new network
void switchToOperationalMode();



void setup() {
  Serial.begin(9600);
  Serial.println("starting up!");

  //switchToSetupMode();
  switchToOperationalMode();

    //Handler for http requests for requests

  server.on("/command", handleCommand);

  server.on("/", handleRoot);

  server.begin();

  Serial.print("Local: ");
  Serial.print(WiFi.localIP());
  
}

void loop() {
 
  server.handleClient();

  delay(1000); 
  

  //Serial.println(cmdSelected);

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


  WiFi.begin(ssidCentral, passwordCentral);
  
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

int sendMessage(String msg) {
  Serial.print(msg);

  return 0;
}


// Tester helper
void handleRoot() {
  Serial.print("\n");
  Serial.println("pinged correctly at root");
  server.send(200, "text/plain", "hello from esp8266!");
}

void printArgs() {
  String message = " ";
  for (int i = 0; i < server.args(); i++) {

     message += "Arg nº" + (String)i + " –> ";
     message += server.argName(i) + ": ";
     message += server.arg(i) + "\n";
   } 
    
   Serial.println(message);
}

// handles a generic command and parses the argument
void handleCommand() {

 Serial.println("pinged correctly at command");
 String test = server.arg("cmd");
 Serial.println(test);
  

  server.send(200, "text/plain", "ACK");
}
