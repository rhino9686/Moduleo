## script for testing ESP8266 Server with HTTPS and Socket communication
import asyncio
import websockets

## This data packet is placeholder data for a hypothetical air quality/Temp/Humidity Sensor 
class dataPacket:
    airQual = 100
    humidity = 20
    temperature = 30
    battLife = 70


class virtualTank:
    currentSpeed = 0
    goingForward = True
    dataStatus = None

    def __init__(self):
        self.currentSpeed = 0
        self.goingForward = True
        self.dataStatus = dataPacket()


