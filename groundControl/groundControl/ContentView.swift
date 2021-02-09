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
                Spacer()
                Button("Turn Left "){
                    sendTurnLeftCommand()
                }
                .foregroundColor(.white)
                .padding()
                .background(Color.blue)
                .cornerRadius(8)
                Spacer()
                Button("     Stop    "){
                    sendHaltCommand()
                }
                .foregroundColor(.white)
                .padding()
                .background(Color.gray)
                .cornerRadius(8)
                Spacer()
                
                Button("Turn Right"){
                    sendTurnRightCommand()
                }
                .foregroundColor(.white)
                .padding()
                .background(Color.blue)
                .cornerRadius(8)
                Spacer()
                
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
