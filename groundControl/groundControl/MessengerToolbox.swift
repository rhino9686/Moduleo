//
//  MessengerToolbox.swift
//  groundControl
//
//  Created by Robert Cecil on 1/18/21.
//

import Foundation
import SwiftUI


enum CommandType: String {
    case movement = "movement"
    case dataScan = "dataScan"
}

enum MoveDirection: String {
    case forward = "forward"
    case back = "backward"
    case turnleft = "turnLeft"
    case turnright = "turnRight"
}

enum ScanType {
    case airQual
    case Humidity
}

// We will just make a high-level Messenger object and tie it to the root view
// will just be an object-oriented version of below functions


final class Messenger: ObservableObject {
    @Published var myInt = 1
    
    private var urlString: String;
    private var url: URL;
    private var port: String = "5000";
    
    private var HTTPResponse = "Nothing Received";
    
    // Constructor: creates a url packet to create requests with repeatedly
    init(ipAddr: String, port: Int?) {
        
        if (port != nil){
            self.port = String(port!);
        }
        
        self.urlString =  "http://" + ipAddr + ":" + self.port;
        self.url = URL(string: urlString)!
    }
    
    
    func sendMessage(cmdType: CommandType, movement: MoveDirection?, scanType: ScanType? ){
        
        var localRequest = URLRequest(url: url)
        
        // Configure request authentication
        localRequest.setValue(
            "authToken",
            forHTTPHeaderField: "Authorization"
        )
        
        // Serialize HTTP Body data as JSON
        let body = ["cmd": cmdType]
        let bodyData = try? JSONSerialization.data(
            withJSONObject: body,
            options: []
        )
        
        // Change the URLRequest to a POST request
        localRequest.httpMethod = "POST"
        localRequest.httpBody = bodyData
        
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

func sendHTTP_POST(_ url_str: String, _ command: String) -> Void {
    
    print("sending command")
    
    let urlString =  "http://" + "192.168.86.208"
    
    let url = URL(string: urlString)!
    

    var request = URLRequest(url: url)
    
    // Configure request authentication
    request.setValue(
        "authToken",
        forHTTPHeaderField: "Authorization"
    )

    // Serialize HTTP Body data as JSON
    let body = ["cmd": command]
    let bodyData = try? JSONSerialization.data(
        withJSONObject: body,
        options: []
    )

    // Change the URLRequest to a POST request
    request.httpMethod = "POST"
    request.httpBody = bodyData
    
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
    
}



// Placeholder HTTP implementations to use with Wi-Fi chip in meantime
func sendForwardCommandHTTP() -> Void {
    sendHTTP_POST("www.placeholder", "Forward")
}

func sendBackWardCommandHTTP() -> Void {
    sendHTTP_POST("www.placeholder", "Backward")
}

func sendTurnLeftCommandHTTP() -> Void {
    sendHTTP_POST("www.placeholder", "Turnleft")
}

func sendTurnRightCommandHTTP() -> Void {
    sendHTTP_POST("www.placeholder", "Turnright")
}

func sendHaltCommandHTTP() -> Void {
    sendHTTP_POST("www.placeholder", "Halt")
}


// Func to use a socket and send a command efficiently
func sendCommandSocket( socketHandle: Int32,  cmd: MoveDirection) {
    
}
