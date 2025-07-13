//
//  MessengerToolbox.swift
//  groundControl
//
//  Created by Robert Cecil on 1/18/21.
//

import Foundation
import SwiftUI
import Starscream



// Tells what kind of message is being sent to executor board
enum CommandType: String {
    case movement = "M"
    case dataScan = "D"
    case speedChange = "S"
}

// Tells what direction to move drone in
enum MoveDirection: String {
    case forward = "F"
    case back = "B"
    case turnleft = "L"
    case turnright = "R"
    case halt = "H"
}

// Tells what sensor to query for data
enum ScanType: String {
    case airQual = "A"
    case Humidity = "H"
    case ambientLight = "L"
}

// Validates a proper IP addr when entered by user
func isValidIP(s: String) -> Bool {
    let parts = s.components(separatedBy: ".")
    let nums = parts.compactMap { Int($0) }
    return parts.count == 4 && nums.count == 4 && nums.filter { $0 >= 0 && $0 < 256}.count == 4
}

// We will just make a high-level Messenger object and tie it to the root view
// will just be an object-oriented version of below functions

final class Messenger: ObservableObject {
    @Published var myInt = 1
    var myIP: String;
    private var urlString: String; //For HTTP
    private var socketUrlString: String; //For Socket
    
    private var port: String = "80";
    private var url: URL;
    private var socketURL: URL;
    
    private var HTTPResponse: String = "Nothing Received";
    
    private var socket: WebSocket;
    
    private var isConnected: Bool;
    
    
    var speedTimer: Timer? = nil;
    private var speedChangedFlag: Bool = false;
    private var speed: UInt8 = 0;
    
    
    // Constructor: creates a url packet to create requests with, repeatedly
    init(ipAddr: String, port: Int?) {
        
        if (port != nil){
            self.port = String(port!);
        }
        self.myIP = ipAddr;
        self.urlString =  "http://" + ipAddr + ":" + self.port;
        self.socketUrlString =  "ws://" + ipAddr + ":" + self.port;
        self.url = URL(string: urlString)!
        self.socketURL = URL(string: socketUrlString)!
        
        self.isConnected = false;
        
        //Assuming we set up URL correctly
        var request = URLRequest(url: self.socketURL);
        request.timeoutInterval = 5;
        self.socket = WebSocket(request: request);
        
        registerSocket(); //load up the socket event handler
        
        //This timer will catch when we change the speed on the slider. it filters it to only trigger on the final value instead of every incremental step of the slider
        self.speedTimer = Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { timer in
            
            if (self.speedChangedFlag){
                self.sendMessage(cmdType: .speedChange, movement: nil, speedVal: self.speed);
                self.speedChangedFlag = false;
            }
            
        }
        
        
        self.socket.connect();
        
        
        
    }
    
    func setURL(ipAddr:String){
        
        self.socket.disconnect();
        
        self.myIP = ipAddr;
        self.urlString =  "http://" + ipAddr + ":" + self.port;
        self.socketUrlString =  "ws://" + ipAddr + ":" + "81";
        self.url = URL(string: urlString)!
        self.socketURL = URL(string: socketUrlString)!
        
        
        //Assuming we set up URL correctly
        var request = URLRequest(url: self.socketURL);
        request.timeoutInterval = 5;
        self.socket = WebSocket(request: request);
        
        registerSocket(); //load up the socket event handler
        
        self.socket.connect();
        
    }
    
    func setSpeed(speed_in: UInt8){
        self.speed = speed_in;
        self.speedChangedFlag = true;
    }
    
    
    func registerSocket(){
        
        self.socket.onEvent = { event in
            switch event {
            case .connected(let headers):
                self.isConnected = true
                print("websocket is connected: \(headers)")
            case .disconnected(let reason, let code):
                self.isConnected = false
                print("websocket is disconnected: \(reason) with code: \(code)")
            case .text(let string):
                print("Received text: \(string)")
            case .binary(let data):
                print("Received data: \(data.count)")
            case .ping(_):
                break
            case .pong(_):
                break
            case .viabilityChanged(_):
                break
            case .reconnectSuggested(_):
                break
            case .cancelled:
                self.isConnected = false
            case .error(_):
                self.isConnected = false
            case .peerClosed:
                break
            }
        }
        
    }
    
    //New Messenger for SocketIO 
    func sendMessage(cmdType: CommandType, movement: MoveDirection?, scanType: ScanType? = nil, speedVal: UInt8? = nil ){
        
        var cmdByte: UInt8 = 0;
        var magByte: UInt8 = 0;
        var dataByte: UInt8 = 0;
        let terminationByte: UInt8 = 0;
        
        if cmdType == .movement
        {
            print("movement command")
            switch movement {
            case .forward:
                cmdByte = 70;  //70  == 'F'
            case .back:
                cmdByte = 66; //66 == 'B'
            case .turnleft:
                cmdByte = 76; //76 == 'L'
            case .turnright:
                cmdByte = 82; //82 == 'R'
            case .halt:
                cmdByte = 72; //72 == 'H'
            case .none:
                return
            }
            
        }
        if cmdType == .speedChange{
            print("speed change!");
            
            cmdByte = 83; // 83 == 'S'
            
            if (speedVal == nil){ //Double checking we don't accidentally call a speed change with null value
                print("Error: speed value is nil but speedChange was called");
                return
            }
            
            //var speedvalChar = String(Character(UnicodeScalar(speedVal!))); //ugly conversion from uint8 to string
            
           // speedvalChar = "\(speedVal!)";
            
            magByte = speedVal!;
            
        }
        if cmdType == .dataScan{
            
            cmdByte = 68; // 68 == 'D'
        }
        
        
       // let finalString: String = cmdByte + magByte + dataByte + terminationByte;
        
        
        var byteArray: [UInt8] = [70, 65, 99, 100];
        
        
        byteArray[0] = cmdByte;
        byteArray[1] = magByte;
        byteArray[2] = dataByte;
        byteArray[3] = terminationByte;
        
        
        self.socket.write(data: Data(byteArray));
        
        //self.socket.write(string: finalString, completion: nil)
        
    
        
    }
    
    
    
    //LEGACY for HTTP
    func HTTPsendMessage(cmdType: CommandType, movement: MoveDirection?, scanType: ScanType? = nil, speedVal: Int8? = nil ){
        
        
        if cmdType == .movement
        {
            let urlLocal = urlString + "/command"
            self.url = URL(string: urlLocal)!
        }
        var localRequest = URLRequest(url: self.url)
        
        // Configure request authentication
        localRequest.setValue(
            "authToken",
            forHTTPHeaderField: "Authorization"
        )
        /* Serialize HTTP Body data as JSON
        let body = ["cmdType": cmdType]
        let bodyData = try? JSONSerialization.data(
            withJSONObject: body,
            options: []
        )
        */
      //  let urlLocal = "http://" + "192.168.1.88:80/command"
 
        var components = URLComponents(url: self.url, resolvingAgainstBaseURL: false)!
        components.queryItems = [
            URLQueryItem(name: "cmd", value: movement?.rawValue)
        ]

        let query = components.url!.query
        // Change the URLRequest to a POST request
        localRequest.httpMethod = "POST"
        localRequest.httpBody =  Data(query!.utf8)
        
        let session = URLSession.shared
        let task = session.dataTask(with: localRequest) { (data, response, error) in

            if error != nil{
                // Handle HTTP request error
                print("error")
            } else if data != nil {
                // Handle HTTP request response
                
                guard let data = data else {
                    print("Empty Data")
                    return
                }
                do {
                    /*
                    let result = try JSONSerialization.jsonObject(with: data, options: .allowFragments) as? [String:AnyObject]
                    if result != nil && ("cmd" != "null") {
                        let Val = result?["cmd"] as! String
                        self.HTTPResponse = Val;
                    }*/
                    // Handle HTTP request response
                    print(data);
                    print("Data is true")
                }
            } else {
                // Handle unexpected error
                print("unknown occurrence")
            }
        }
        task.resume()
    }
}


// Initial style of messages will be HTTP Request
func sendHTTP_POST(_ url_str: String, _ command: String, _ numeric: Int = 0) -> Void {
    
    print("sending command")
    
    let urlString =  "http://" + "192.168.1.88:80/command"
    
    let url = URL(string: urlString)!
    
    var request = URLRequest(url: url)
    
    // Configure request authentication
    request.setValue(
        "authToken",
        forHTTPHeaderField: "Authorization"
    )

    // Serialize HTTP Body data as JSON (this seems to add unnecessary JSON artifacts that the arduino libraries don't work with, replaced with the URLcomponents method
    /*
    
    let body:[String: Any] = ["cmd": command, "name": "jack and jill"]
    let bodyData = try? JSONSerialization.data(
        withJSONObject: body,
        options: .prettyPrinted
    )
   */
    
    var components = URLComponents(url: url, resolvingAgainstBaseURL: false)!
    components.queryItems = [
        URLQueryItem(name: "cmd", value: command),
        URLQueryItem(name: "key2", value: "blooo")
    ]

    let query = components.url!.query

    
    // Change the URLRequest to a POST request
    request.httpMethod = "POST"
    request.httpBody = Data(query!.utf8)
    
    let session = URLSession.shared
    let task = session.dataTask(with: request) { (data, response, error) in

        if error != nil{
            // Handle HTTP request error
            print("error")
        } else if data != nil {
            // Handle HTTP request response
            print("Data is true")
        } else {
            // Handle unexpected error
            print("unknown occurrence")
        }
    }
    task.resume()
    
}

// Top level handle for sending commands to Wi-Fi boards
// Will replace with Sockets to improve efficiency
func sendForwardCommand() -> Void {
    sendForwardCommandHTTP()
}

func sendBackWardCommand() -> Void {
    sendBackWardCommandHTTP()
}

func sendTurnLeftCommand() -> Void {
    sendTurnLeftCommandHTTP()
}

func sendTurnRightCommand() -> Void {
    sendTurnRightCommandHTTP()
}

func sendHaltCommand() -> Void {
    sendHaltCommandHTTP()
}

func sendSpeedUpdate(newSpeedVal: Int) -> Void {
    sendSpeedUpdateHTTP(newSpeedVal: 3)
}



// Placeholder HTTP implementations to use with Wi-Fi chip in meantime
func sendForwardCommandHTTP() -> Void {
    sendHTTP_POST("www.placeholder", MoveDirection.forward.rawValue)
}

func sendBackWardCommandHTTP() -> Void {
    sendHTTP_POST("www.placeholder", MoveDirection.back.rawValue)
}

func sendTurnLeftCommandHTTP() -> Void {
    sendHTTP_POST("www.placeholder", MoveDirection.turnleft.rawValue)
}

func sendTurnRightCommandHTTP() -> Void {
    sendHTTP_POST("www.placeholder", MoveDirection.turnright.rawValue)
}

func sendHaltCommandHTTP() -> Void {
    sendHTTP_POST("www.placeholder", MoveDirection.halt.rawValue)
}


func sendSpeedUpdateHTTP(newSpeedVal: Int) -> Void {
    sendHTTP_POST("www.placeholder", "S", newSpeedVal)
}

// Func to use a socket and send a command efficiently
func sendCommandSocket( socketHandle: Int32,  cmd: MoveDirection) {
    
}
