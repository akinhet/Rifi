//
//  ViewController.swift
//  iOS_RIFI
//
//  Created by Aayush Pokharel on 2020-03-17.
//  Copyright © 2020 Aayush Pokharel. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    
    // refrencing storyboard elements
    @IBOutlet weak var ipField: UITextField!
    
    
    @IBAction func manualButton(_ sender: Any) {
        if (ipField.text!.count > 6 && (ipField.text?.split(separator: ".").count)! > 3) {
            performSegue(withIdentifier: "webPage", sender: sender)
        }else{
           ipField.text = "err!"
        }
        
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()

        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(UIInputViewController.dismissKeyboard))
        view.addGestureRecognizer(tap)

    }

    
    @objc func dismissKeyboard() {
        view.endEditing(true)
    }
    
        override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
            if segue.identifier == "webPage" {
                let controller = segue.destination as! WebPageViewController
                controller.pageURL = "http://\(ipField.text!):8000"
                ipField.text = ""
            }
        }



}

