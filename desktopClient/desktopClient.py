## script for testing ESP8266 Server with HTTPS and Socket communication
import websockets
import asyncio
import flask

quitCmd = "Q"

ipAddr = "192.777.345"

port = "80"

urlStr = "http://" + ipAddr + ":" + port
 

async def hello():
    async with websockets.connect(urlStr) as websocket:
        await websocket.send("Hello world!")
        await websocket.recv()



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