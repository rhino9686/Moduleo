//
//  ConnectionView.swift
//  groundControl
//
//  Created by Robert Cecil on 12/24/23.
//

import SwiftUI


let myGrey = Color(red: (30/255), green: (30/255), blue: (30/255), opacity: 1.0)

struct ConnectionView: View {
    //Our tank Data packet
    //@EnvironmentObject var tankData: TankProfile
    
    //String vars to display things easier
    @State var currentTempStr = "70 °F"
    @State var currentpHStr = "6.03"
    @State var lastTimeChecked = "3 hours ago"
    @State var overallConnection = "Good"
    @State var warningString = ""
    
    //Colors to dislpay things, to show health of system
    @State var healthColor: Color = .green
    @State var tempColor: Color = .blue
    @State var pHColor: Color = .blue
    
    //Timer to get the "last time checked" to update by itself
    let timer = Timer.publish(every: 20, on: .main, in: .common).autoconnect()
    
    
    func update() {
        print("updating")
     //   self.tankData.updateParams()
       
    }
    
    var body: some View {
        
        VStack {
            HStack {
                Text("Connection: ")
                    .font(.title)
                    .fontWeight(.medium)
                Text(overallConnection)
                    .font(.title)
                    .foregroundColor(healthColor)
                Spacer()
            }
            .padding(.top)
            HStack {
                Text(self.warningString)
                    .font(.footnote)
                    .foregroundColor(.yellow)
                Spacer()
            }.padding(.top,3)
            
            
            HStack {
                Text("Last checked: \(self.lastTimeChecked)")
                    .onReceive(timer) { input in
                        
                        //print("ticktock");
   
                }
                    .font(.footnote)
                
                Spacer()

                Button(action: {
                   
                }, label: {
                    Image(systemName: "arrow.clockwise")
                })
                    .foregroundColor(Color.white)
                    .padding(10)
                .background(myGrey)
                .onTapGesture {  self.update() } //This updates Temp, pH, time
                .cornerRadius(5)
                .padding(.trailing)
                
            }
       
            HStack {
                Text("Temperature: ")
                Text("\(self.currentTempStr)")
                    .foregroundColor(tempColor)

                Spacer()
            }
            .padding(.top, 5)
     
            
            //pH label
            HStack {
                Text("Air Quality: ")
                Text("\(self.currentpHStr)")
                    .foregroundColor(pHColor)
                Spacer()
            }
            .padding(.top).padding(.bottom)
            
            
            
        }
        .padding(30)
    }
}


#Preview {
    ConnectionView()
}
