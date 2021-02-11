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

// controls view for settings 
struct SettingsView: View {
    @EnvironmentObject var messenger: Messenger
    
    @State private var newIP: String = "";
    @State private var isEditing = false
    
    init() {
     //   username = messenger.myIP;
    }
    
    var body: some View {
        
        VStack {
            Spacer()
            Text("Current IP Address:  " + messenger.myIP)
            Spacer()
            
            TextField(
               "     Enter new IP address",
                text: $newIP
           ) { isEditing in
               self.isEditing = isEditing
           } onCommit: {
            
                let result = isValidIP(s: newIP)
                if result {
                    messenger.setURL(ipAddr: newIP)
                }
            
           }
           .autocapitalization(.none)
           .disableAutocorrection(true)
           .border(Color(UIColor.separator))
           Text(newIP)
               .foregroundColor(isEditing ? .red : .blue)
            Spacer()
        }.padding()
           
        
    }
}

struct ContentView: View {
    //controls state of popup modal
    @State private var showingSettings = false
    
    @EnvironmentObject var messenger: Messenger
    @State var speed: Double = 20
    
    func speedChanged(to value: Double) {
        print("Name changed to \(speed)!")
      //  var intSpeedVal = Int32(speed);
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
      
        Button("Preferences") {
            showingSettings.toggle()
        }.padding(10)
        .sheet(isPresented: $showingSettings) {
            SettingsView().environmentObject(self.messenger)
        }
        
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
