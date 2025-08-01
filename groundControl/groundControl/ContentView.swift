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
        //Do I even need this?
        //maybe for speed or something later
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
            Button("Set IP to 192.168.4.96"){
                
                messenger.setURL(ipAddr: "192.168.4.96")
                
            }
            Spacer()
            Button("Set IP to 192.168.4.99"){
                
                messenger.setURL(ipAddr: "192.168.4.99")
                
            }
            Spacer()
            Button("Set IP to 192.168.4.82"){
                
                messenger.setURL(ipAddr: "192.168.4.82")
                
            }
            Spacer()
            
        }.padding()
           
        
    }
}

struct ContentView: View {
    //controls state of popup modal
    @State private var showingSettings = false
    
    @EnvironmentObject var messenger: Messenger
    @State var speed: Double = 20
    @State private var speedChangedFlag: Bool = false
    
    func speedChanged(to value: Double) {
        
        let speedInt: UInt8 = UInt8(speed);
        print("Speed changed to \(speedInt)");
        messenger.setSpeed(speed_in: speedInt);
        
    }
    
    func updateSpeed(){
        
        if (speedChangedFlag){
            let speedInt: UInt8 = UInt8(speed);
            messenger.sendMessage(cmdType: .speedChange, movement: nil, speedVal: speedInt);
            
        }
    }
    
    var speedTimer: Timer? = nil
    
    init() {
        
        //We moved the timer logic inside the messenger class and connection status so this is vestigial for now
        self.speedTimer = Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { timer in
            
            
                let randomNumber = Int.random(in: 1...20)
               // print("Number: \(randomNumber)")

                if randomNumber == 10 {
                    timer.invalidate()
                }
        }

    }
    
    
    var body: some View {
        VStack{
            ConnectionView()
            Text("Controls")
                .bold()
                .font(.title)
                .padding()
            
            Button("Go Forward"){
                
                messenger.sendMessage(
                    cmdType:  .movement,
                    movement: .forward)
                
            }
            .foregroundColor(.white)
            .padding()
            .background(Color.blue)
            .cornerRadius(8)
            HStack{
                Spacer()
                Button(" Turn Left  "){
                   // sendTurnLeftCommand()
                    
                    messenger.sendMessage(
                        cmdType:  .movement,
                        movement: .turnleft)
                }
                .foregroundColor(.white)
                .padding()
                .background(Color.blue)
                .cornerRadius(8)
                Spacer()
                Button("Stop"){
                //    sendHaltCommand()
                    messenger.sendMessage(
                        cmdType:  .movement,
                        movement: .halt)
                }
                .foregroundColor(.white)
                .padding()
                .padding(Edge.Set.trailing, 20)
                .padding(Edge.Set.leading, 20)
                .background(Color.gray)
                .cornerRadius(8)
                
                Spacer()
                
                Button("Turn Right"){
                //    sendTurnRightCommand()
                    messenger.sendMessage(
                        cmdType:  .movement,
                        movement: .turnright)
                }
                .foregroundColor(.white)
                .padding()
                .background(Color.blue)
                .cornerRadius(8)
                Spacer()
                
            }
            Button("Go Backward"){
                
                //sendBackWardCommand()
                messenger.sendMessage(
                    cmdType:  .movement,
                    movement: .back)
                
            }
            .foregroundColor(.white)
            .padding()
            .background(Color.blue)
            .cornerRadius(8)
            
            
            Text("Speed")
                .font(.title)
                .padding()
            
            Slider(value: $speed.onChange(speedChanged), in: 0...100).padding(30)
       
            
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
