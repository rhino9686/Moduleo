//
//  ContentView.swift
//  groundControl
//
//  Created by Robert Cecil on 1/17/21.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack{
            
            Text("Controls")
                .bold()
                .padding()
            
            Button("Forward"){
                
                sendForwardCommand()
                
            }
            .foregroundColor(.white)
            .padding()
            .background(Color.blue)
            .cornerRadius(8)
            HStack{
                
                Button("Left "){
                    sendTurnLeftCommand()
                }
                .foregroundColor(.white)
                .padding()
                .background(Color.blue)
                .cornerRadius(8)
                
                Button("Right"){
                    sendTurnRightCommand()
                }
                .foregroundColor(.white)
                .padding()
                .background(Color.blue)
                .cornerRadius(8)
                
            }
            Button("Backwards"){
                
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
