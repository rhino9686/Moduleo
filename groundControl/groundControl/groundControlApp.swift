//
//  groundControlApp.swift
//  groundControl
//
//  Created by Robert Cecil on 1/17/21.
//

import SwiftUI

@main
struct groundControlApp: App {
    
    let messenger = Messenger(ipAddr: "192.168.1.88", port: 80);
    
    var body: some Scene {
        WindowGroup {
            ContentView().environmentObject(self.messenger)
        }
    }
}
