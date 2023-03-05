//
//  ContentView.swift
//  MakeOhioApp
//
//  Created by Pranav Chati on 3/4/23.
//

import MapKit

import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = ContentViewModel()
    
    
    var body: some View {
        Map(coordinateRegion: $viewModel.region, showsUserLocation: true,  userTrackingMode: .constant(.follow))
            .onAppear {
                viewModel.checkIfLocationServicesIsEnabled()
            }
            .overlay(
                Circle()
                    .stroke(Color.pink, lineWidth: 2)
                    .opacity(0.8)
                    .frame(width: 400, height: 400)
            )
            .ignoresSafeArea()
            .accentColor(Color(.systemPink))
            

    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
        
    }
}


