//
//  ContentView.swift
//  groundControl
//
//  Created by Robert Cecil on 1/17/21.
//

import SwiftUI

struct ContentView: View {
    @EnvironmentObject var messenger: Messenger
    
    var body: some View {
        VStack{
            
            Text("Controls")
                .bold()
                .padding()
            
            Button("Go Forward"){
                
                sendForwardCommand()
                
            }
            .foregroundColor(.white)
            .padding()
            .background(Color.blue)
            .cornerRadius(8)
            HStack{
                
                Button("Turn Left "){
                    sendTurnLeftCommand()
                }
                .foregroundColor(.white)
                .padding()
                .background(Color.blue)
                .cornerRadius(8)
                
                Button("Turn Right"){
                    sendTurnRightCommand()
                }
                .foregroundColor(.white)
                .padding()
                .background(Color.blue)
                .cornerRadius(8)
                
            }
            Button("Go Backward"){
                
                sendBackWardCommand()
                
            }
            .foregroundColor(.white)
            .padding()
            .background(Color.blue)
            .cornerRadius(8)
            
        }
        
        
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
