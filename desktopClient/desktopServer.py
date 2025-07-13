## script for testing ESP8266 Server with HTTPS and Socket communication
import asyncio
import websockets
import socket
from websockets.server import serve
import virtualTank

quitCmd = "Q"
ipAddr="192.168.4.82"
port = "81"

urlStr = "ws://" + ipAddr + ":" + port
 
## creating virtual tank to talk to iPhone App as dummy
myTank = virtualTank()

async def echo(websocket):
    async for message in websocket:
        await process_message(message)


async def hello():
    async with websockets.connect(urlStr) as websocket:
        newtxt = await websocket.recv()
        await websocket.send("Hello world!")
        newtxt = await websocket.recv()
        print(newtxt)


async def process_message(message):
    print("received message!")
    
    split = [i for i in message]
    print(message)
    print(split)
    return


async def asyncMain():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever




async def handleCommand(dataArr):

    
    return



def main():
    exiting = False

    while (not exiting):

     txt = input("Type something to test this out: ")
     print("Is this what you just said? ", txt)

     if txt == "H":
         myIpAddr = socket.gethostbyname(socket.gethostname())
         print(myIpAddr)
         asyncio.run(asyncMain())


     if txt == "Q":
         exiting = True
         print("Goodbye!")
         exit()



if __name__ == "__main__":
    main()