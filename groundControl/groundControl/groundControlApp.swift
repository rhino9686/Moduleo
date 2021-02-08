//
//  groundControlApp.swift
//  groundControl
//
//  Created by Robert Cecil on 1/17/21.
//

import SwiftUI

@main
struct groundControlApp: App {
    
    let messenger = Messenger(ipAddr: "343.434.433.233", port: 80);
    
    var body: some Scene {
        WindowGroup {
            ContentView().environmentObject(messenger)
        }
    }
}
