## script for testing ESP8266 Server with HTTPS and Socket communication
import websockets
import socket
import asyncio
import tkinter as tk
from tkinter import ttk

#keyboard command to quit applications (placeholder for GUI buttons)
quitCmd = "Q"
ipAddr = "192.168.4.82"
port = "81"

urlStr = "ws://" + ipAddr + ":" + port
 

# Base "root application", inherits from tk.tk, should be parent of any frame classes
class TkApp(tk.Tk):
    def __init__(self):
        super().__init__()

        ##give ourselves a title
        self.title("Home Base")


    

class TkFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
    

##placeholder function for async socket example
async def hello():
    async with websockets.connect(urlStr) as websocket:
        newtxt = await websocket.recv()
        await websocket.send("Hello world!")
        newtxt = await websocket.recv()
        print(newtxt)


def main():

    app = TkApp()
    app.mainloop()

    """
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
"""


if __name__ == "__main__":
    main()