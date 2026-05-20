
#include <WiFi.h>
#include <ArduinoOTA.h>
#include "privates.h"
#include "Robot.h"
#include <WebSocketsServer.h>


WebSocketsServer webSocket = WebSocketsServer(81);

//Set USE_SERIAL=Serial to see all output on Serial Monitor, Set USE_SERIAL=mySerial to turn off extra output (extra output will be seen by STM32 UART)
//#define USE_SERIAL Serial 
#define USE_SERIAL Serial

#define STM32 Serial1

//These are really just for the mySerial Swap, to adjust our output, kinda hacky
const byte rxPin = 12;
const byte txPin = 3;

//This is for outputting on onboard LED when the connection is secure
const byte outputLightPin = 2;
const byte outputLightPin2 = 13;

bool ISCONNECTED = 0;

RobotTank myRobot;

void processTextPayload(uint8_t * payload, size_t length);

bool testRobotConnection(int input);

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {

    switch(type) {
        case WStype_DISCONNECTED:
            USE_SERIAL.printf("[%u] Disconnected!\n", num);
              //send a halt command to Robot if app disconnects
              STM32.print('H');
              STM32.write(0);
              STM32.print('Z');
              STM32.print('Z');
              //external PCB LED set dark
              analogWrite(outputLightPin2, 0);
            break;
        case WStype_CONNECTED:
            {
                IPAddress ip = webSocket.remoteIP(num);
                USE_SERIAL.printf("[%u] Connected from %d.%d.%d.%d url: %s\n", num, ip[0], ip[1], ip[2], ip[3], payload);
                //External PCB LED set bright
                analogWrite(outputLightPin2, 200);
				
				// send message to client
				webSocket.sendTXT(num, "Connected");
            }
            break;
        case WStype_TEXT:
            USE_SERIAL.printf("[%u] get Text: %s\n", num, payload);

            // send message to client
            webSocket.sendTXT(num, "Command Received");

            processTextPayload(payload, length);

            
            break;
        case WStype_BIN:
            USE_SERIAL.printf("[%u] get binary length: %u\n", num, length);
           // hexdump(payload, length);

            // send message to client
            // webSocket.sendBIN(num, payload, length);
            processTextPayload(payload, length);
            break;
    }

}

void setup() {
   // USE_SERIAL.begin(38400);ß
    Serial1.begin(38400, SERIAL_8N1, 18, 17); // RX=GPIO18, TX=GPIO17 (pick your pins)

    USE_SERIAL.println();
    USE_SERIAL.println();
    USE_SERIAL.println();

    for(uint8_t t = 4; t > 0; t--) {
        USE_SERIAL.printf("[SETUP] BOOT WAIT %d...\n", t);
        USE_SERIAL.flush();
        delay(1000);
    }

    WiFi.mode(WIFI_STA);
    WiFi.begin(corey_ap, corey_password);


    while(WiFi.status() != WL_CONNECTED) {
        USE_SERIAL.printf("connecting to WiFi");
        delay(100);
    }
    USE_SERIAL.printf("connected to WiFi!\n");
    USE_SERIAL.print("ESP32 Web Server's IP address: ");
    USE_SERIAL.println(WiFi.localIP().toString().c_str());

    // testing the connection between STM32 and ESP8266
    bool isConnected = 0;
    bool first_test = 0;
    bool second_test = 0;
    // this pin is ACTIVE LOW so 255 makes it off, and 0-254 is on. We are turning it OFF until handshake is complete
    analogWrite(outputLightPin, 255);


   // isConnected = 1;  //TOGGLE THIS OFF TO ENABLE THE HANDSHAKE

    while (!isConnected){
      bool first_test = testRobotConnection(100);
      bool second_test = testRobotConnection(200);

      if (!first_test){
        USE_SERIAL.print("First Test failed");
        analogWrite(outputLightPin, 255);
      }
      if (!second_test){
        USE_SERIAL.print("Second Test failed");
      }
      delay(500);
      isConnected = ( first_test || second_test);
      USE_SERIAL.print("Trying to Connect\n");
      analogWrite(outputLightPin, 5);
    }
    bool third_test = testRobotConnection(101);
    //If we've gotten here, then the two boards are connected
    analogWrite(outputLightPin, 5);
    ISCONNECTED = 1;

    webSocket.begin();
    webSocket.onEvent(webSocketEvent);

    
}

void loop() {
    webSocket.loop();
    if(ISCONNECTED){
      analogWrite(outputLightPin, 5);
     
    }
   // delay(1000);
}


void processTextPayload(uint8_t * payload, size_t length){

  //convert the payload into it's four bytes of data
  char cmdByte = (char)payload[0];

  int magByteInt = payload[1];

  char dataByte = (char)payload[2];

  char termByte = (char)payload[3];


  //Temperature or humidity data will inrease size of payload data array

  dataByte = 'Z';

  termByte = 'Z';


  //validate the data here

  bool validCMD = (cmdByte == 'H' || cmdByte ==  'S' || cmdByte == 'R' || cmdByte == 'L' || cmdByte == 'F' || cmdByte == 'D');

  // if (validCMD) {}
  //if everything is fine, send to STM32
  STM32.print(cmdByte);
  STM32.write(magByteInt);
  STM32.print(dataByte);
  STM32.print(termByte);
  //STM32.print('\n'); // For seeing debug output neatly, can remove later

  //Save everything in robot data struct?

  if (cmdByte == 'S'){
    myRobot.speed = magByteInt;
  }

  else if (cmdByte == 'D'){
    //Do something with data
  }
  else{
     myRobot.direction = cmdByte;
  }



  return;
}

bool testRobotConnection(int input){
  int data_rcvd = 0;
  bool passed = 0;

  STM32.write(input);
  STM32.print('Z');
  STM32.print('Z');
  STM32.print('Z');
  
  delay(2000);

  if(STM32.available()) {
    data_rcvd = STM32.read();   // read one byte from serial buffer and save to data_rcvd
  }

  passed = (data_rcvd == input);

  if (passed) {
    return 1;
  }

  return 0;

}



