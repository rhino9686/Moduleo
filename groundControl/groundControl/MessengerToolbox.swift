//
//  MessengerToolbox.swift
//  groundControl
//
//  Created by Robert Cecil on 1/18/21.
//

import Foundation


// Initial style of messages will be HTTP Request

func sendHTTP_POST(_ url_str: String, _ command: String) -> Void {
    
    let url = URL(string: url_str)!
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
        } else {
            // Handle unexpected error
            print("unknown occurrence")
        }
    }
    
    task.resume()
    
}



func sendForwardCommand() -> Void {
    
    sendHTTP_POST("www.placeholder", "Forward")
    
}


func sendBackWardCommand() -> Void {
    
    sendHTTP_POST("www.placeholder", "Backward")
    
}


func sendTurnLeftCommand() -> Void {
    
    sendHTTP_POST("www.placeholder", "Turnleft")
    
}

func sendTurnRightCommand() -> Void {
    
    sendHTTP_POST("www.placeholder", "Turnright")
    
}


