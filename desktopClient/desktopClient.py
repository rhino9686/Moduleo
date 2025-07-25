## script for testing ESP8266 Server with HTTPS and Socket communication
import websockets
import socket
import asyncio
##import flask

quitCmd = "Q"


ipAddr="192.168.4.82"

port = "81"

urlStr = "ws://" + ipAddr + ":" + port
 

async def hello():
    async with websockets.connect(urlStr) as websocket:
        newtxt = await websocket.recv()
        await websocket.send("Hello world!")
        newtxt = await websocket.recv()
        print(newtxt)




def main():
    exiting = False

    while (not exiting):
     txt = input("Type something to test this out: ")
     print("Is this what you just said? ", txt)

     if txt == "H":
         
         
         asyncio.run(hello())


     if txt == "Q":
         exiting = True
         print("Goodbye!")
         exit()



if __name__ == "__main__":
    main()