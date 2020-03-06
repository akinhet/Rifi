//
//  InterfaceController.swift
//  Remote Controller WatchKit Extension
//
//  Created by Aayush Pokharel on 2020-02-24.
//  Copyright © 2020 Aayush Pokharel. All rights reserved.
//

import WatchKit
import Foundation

var url = ""

class InterfaceController: WKInterfaceController {
    
    @IBOutlet weak var IpPortLabel: WKInterfaceLabel!
    
    @IBOutlet weak var InputGroup: WKInterfaceGroup!
    @IBOutlet weak var doneBtn: WKInterfaceButton!
    
    @IBOutlet weak var showButton: WKInterfaceButton!
    
    
    @IBAction func showBtn() {
        InputGroup.setHidden(false)
        doneBtn.setEnabled(true)
        url = ""
        IpPortLabel.setText("")
        showButton.setHidden(true)
    }
    
    @IBAction func btn1() {
        url += "1"
        IpPortLabel.setText(url)
    }

    @IBAction func btn2() {
        url += "2"
        IpPortLabel.setText(url)
    }
    
    @IBAction func btn3() {
        url += "3"
        IpPortLabel.setText(url)
    }
    
    @IBAction func btn4() {
        url += "4"
        IpPortLabel.setText(url)
    }
    
    @IBAction func btn5() {
        url += "5"
        IpPortLabel.setText(url)
    }
    
    @IBAction func btn6() {
        url += "6"
        IpPortLabel.setText(url)
    }
    
    @IBAction func btn7() {
        url += "7"
        IpPortLabel.setText(url)
    }
    
    @IBAction func btn8() {
        url += "8"
        IpPortLabel.setText(url)
    }
    
    @IBAction func btn9() {
        url += "9"
        IpPortLabel.setText(url)
    }

    
    @IBAction func btnPeriod() {
        url += "."
        IpPortLabel.setText(url)
    }
    
    @IBAction func btn0() {
        url += "0"
        IpPortLabel.setText(url)
    }
    
    @IBAction func btnClear() {
        doneBtn.setEnabled(true)
        url = ""
        IpPortLabel.setText("")
    }
    var newUrl = ""
    
    @IBAction func changeIP() { //note this is for the donw button (green done button)
        InputGroup.setHidden(true)
        showButton.setHidden(false)
        newUrl = "http://" + url;
        url = newUrl;
        url += ":8000/?key=";
        newUrl = url;
        print(newUrl)
    }

    func PostValue(key:String){
        url = newUrl
        url += key
    
        let getURL = URL(string: url)!
            let urlSession = URLSession.shared
            let getRequest = URLRequest(url: getURL)

            let task = urlSession.dataTask(with: getRequest as URLRequest, completionHandler: { data, response, error in
                guard error == nil else {
                    return
                }
            })
            task.resume()
    }
    
    @IBAction func forwardButton() {
        PostValue(key: "right")
    }
    
    @IBAction func backButton() {
        PostValue(key: "left")
    }
    
    @IBAction func playPauseButton() {
        PostValue(key: "space")
    }
    
    @IBAction func volumeUp() {
        PostValue(key: "up")
    }
    
    @IBAction func volumeDown() {
        PostValue(key: "down")
    }
    
    @IBAction func homeButton() {
        PostValue(key: "enter")
    }
    
    @IBAction func mute() {
        PostValue(key: "volumemute")

    }
    @IBAction func power() {
        PostValue(key: "power")

    }
    var initialValue  = 0.0
    @IBAction func volumeSlider(_ value: Double) {
        if (value < initialValue){
            PostValue(key: "down")
            initialValue = value
        }
        if (value > initialValue){
            PostValue(key: "up")
            initialValue = value
        }
    }
    


}
