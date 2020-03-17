//
//  WebPageViewController.swift
//  iOS_RIFI
//
//  Created by Aayush Pokharel on 2020-03-17.
//  Copyright © 2020 Aayush Pokharel. All rights reserved.
//

import UIKit
import WebKit

class WebPageViewController: UIViewController {

    var pageURL : String = ""
    
    @IBOutlet weak var webView: WKWebView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let myUrl  = URL(string: pageURL)
        let myRequest = URLRequest(url: myUrl!)
        webView.load(myRequest)


    }
    


}
