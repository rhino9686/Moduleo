//
//  MessengerToolbox.swift
//  groundControl
//
//  Created by Robert Cecil on 1/18/21.
//

import Foundation
import SwiftUI


// TODO: revise and integrate or drop
enum CommandType: String {
    case movement = "movement"
    case dataScan = "dataScan"
}

// TODO: revise and integrate or drop
enum MoveDirection: String {
    case forward = "forward"
    case back = "backward"
    case turnleft = "turnLeft"
    case turnright = "turnRight"
}

// TODO: Integrate or drop
enum ScanType {
    case airQual
    case Humidity
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
    private var urlString: String;
    private var url: URL;
    private var port: String = "80";
    
    private var HTTPResponse = "Nothing Received";
    
    // Constructor: creates a url packet to create requests with, repeatedly
    init(ipAddr: String, port: Int?) {
        
        if (port != nil){
            self.port = String(port!);
        }
        self.myIP = ipAddr;
        self.urlString =  "http://" + ipAddr + ":" + self.port;
        self.url = URL(string: urlString)!
    }
    
    func setURL(ipAddr:String){
        self.myIP = ipAddr;
        self.urlString =  "http://" + ipAddr + ":" + self.port;
        self.url = URL(string: urlString)!
    }
    
    
    func sendMessage(cmdType: CommandType, movement: MoveDirection?, scanType: ScanType? ){
        
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
        
        var components = URLComponents(url: url, resolvingAgainstBaseURL: false)!
        components.queryItems = [
            URLQueryItem(name: "cmd", value: cmdType.rawValue),
            URLQueryItem(name: "key2", value: "blooo")
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
                    let result = try JSONSerialization.jsonObject(with: data, options: .allowFragments) as? [String:AnyObject]
                    if result != nil && ("cmd" != "null") {
                        let Val = result?["cmd"] as! String
                        self.HTTPResponse = Val;
                    }
                
                } catch {
                       print("Error -> \(error)")
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
    
    let urlString =  "http://" + "192.168.1.88/command"
    
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
    sendHTTP_POST("www.placeholder", "F")
}

func sendBackWardCommandHTTP() -> Void {
    sendHTTP_POST("www.placeholder", "B")
}

func sendTurnLeftCommandHTTP() -> Void {
    sendHTTP_POST("www.placeholder", "L")
}

func sendTurnRightCommandHTTP() -> Void {
    sendHTTP_POST("www.placeholder", "R")
}

func sendHaltCommandHTTP() -> Void {
    sendHTTP_POST("www.placeholder", "H")
}


func sendSpeedUpdateHTTP(newSpeedVal: Int) -> Void {
    sendHTTP_POST("www.placeholder", "S", newSpeedVal)
}

// Func to use a socket and send a command efficiently
func sendCommandSocket( socketHandle: Int32,  cmd: MoveDirection) {
    
}
