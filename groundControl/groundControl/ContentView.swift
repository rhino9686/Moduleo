//
//  ContentView.swift
//  groundControl
//
//  Created by Robert Cecil on 1/17/21.
//

import SwiftUI

//extension to State var (which inherits from Binding) to attach a handler on a changing value
extension Binding {
    func onChange(_ handler: @escaping (Value) -> Void) -> Binding<Value> {
        Binding(
            get: { self.wrappedValue },
            set: { newValue in
                self.wrappedValue = newValue
                handler(newValue)
            }
        )
    }
}

struct ContentView: View {
    @EnvironmentObject var messenger: Messenger
    @State var speed: Double = 20;
    
    func speedChanged(to value: Double) {
        print("Name changed to \(speed)!")
    }
    
    var body: some View {
        VStack{
            
            Text("Controls")
                .bold()
                .font(.title)
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
            
            
            Text("Speed")
                .font(.title)
                .padding()
            
            Slider(value: $speed.onChange(speedChanged), in: 0...30).padding(30)
            Text("Current speed: \(speed, specifier: "%.0f")")
        }
        
        
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
