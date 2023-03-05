//
//  ContentViewModel.swift
//  MakeOhioApp
//
//  Created by Pranav Chati on 3/5/23.
//

import MapKit

final class ContentViewModel1: NSObject, ObservableObject, CLLocationManagerDelegate {
    @Published var region = MKCoordinateRegion(
        center: CLLocationCoordinate2D(
        latitude: 39.992981,
        longitude: -83.001221),
        span: MKCoordinateSpan(
            latitudeDelta: 0.01,
            longitudeDelta: 0.01)
    )
     
    var locationManager: CLLocationManager?
    
    override init() {
        super.init()
        checkIfLocationServicesIsEnabled()
    }

    func checkIfLocationServicesIsEnabled() {
        if CLLocationManager.locationServicesEnabled() {
            locationManager = CLLocationManager()
            locationManager!.delegate = self
            locationManager?.desiredAccuracy = kCLLocationAccuracyBest
            locationManager?.requestWhenInUseAuthorization()
        } else {
            print("Location is not on")
        }
    }
    
    private func checkLocationAuthorization() {
        guard let locationManager = locationManager else { return }
        
        //check for all the cases of the location manager
        switch locationManager.authorizationStatus {
        case .notDetermined:
            break
        case .restricted:
            print(" Your location is restricted.")
        case .denied:
            print ("you have denied your location to be found ")
        case .authorizedAlways, .authorizedWhenInUse:
            if let location = locationManager.location {
                region = MKCoordinateRegion(center: location.coordinate,
                                            span: MKCoordinateSpan(
                                                latitudeDelta: 0.01,
                                                longitudeDelta: 0.01 )
                                            )
            }
            break
        @unknown default:
            break
        }
    }
    
    
//    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
//        DispatchQueue.main.async {
//            self.checkLocationAuthorization()
//        }
//    }
    
    func locationManager(_ manager: CLLocationManager, didChangeAuthorization status: CLAuthorizationStatus) {
        checkLocationAuthorization()
    }
}
