## script for testing ESP8266 Server with HTTPS and Socket communication
import websockets

quitCmd = "Q"

def main():
    exiting = False


    while (not exiting):

     txt = input("Type something to test this out: ")
     print("Is this what you just said? ", txt)
     if txt == "Q":
         exiting = True



if __name__ == "__main__":
    main()