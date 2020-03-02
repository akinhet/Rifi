## **RIFI v1.2**
This is the official repo for Wireless Multimedia controller App/Program "RIFI"

Tested on : MacOS | Windows 10 | Manjaro *Linux*

---

##  [![Watch OS version](https://img.shields.io/badge/WatchOS-6.1-skyblue?style=flat)](https://www.apple.com/ca/watchos/watchos-6/)   [![python 3.8](https://img.shields.io/badge/Python-3.8.1-brightred?style=flat)](https://www.python.org/)   [![ask me why](https://img.shields.io/badge/Rifi-v1.2-purple?style=flat)](http://aayush.wtf)


  Watch Connect and Player View</br>
  <img src="Images/wc.png" width="128" >
  <img src="Images/wp.png" width="128" ></br>
     Phone Web Controler View</br>
  <img src="Images/ips.png" width="256">
</br>

---
**Installation**

 `git clone "repo"` or Download .zip/.tar file from the [releases](https://github.com/Aayush9029/Rifi/releases).

 `cd PythonApp`

 `pip install -r requirements.txt`

Complie the watchApp/Remote Controller.xcodeproj and install in apple watch

*will add a universal in-browser app soon*


### Usage:

> `python main.py` *on the host computer*

> *Select Y on show barcode* > *Scan barcode* > Go to the link.

> (For apple watch app) *Open App > input ip of the computer > Save > Scroll to multimedia.*

---

### So how does this work?

- Python stars a local server *using flask (library)* 
  - Port : 8000 (configurable)
  - ip : Local host ip (eg: 192.168.1.4)
- Listens for Inputs (Play/pause, volume up...)
- Performs the keystrokes in the Laptop that is running flask.



Basically this transforms an Apple Watch to a virtual remote enabling it to controll multimedia.

Uses:

- While Playing a music in laptop (Play/Pause) (Skip) (Volume up/down) 

- While Watching Movie and keyboard/mouse is a bit too far to reach.

- While playing music to skip tracks and since the keystrokes are configurable they can be use to initiate custom shortcuts.

---

To Do:
- Create a separate UI elements for controlling system media controls. *fixes issue #2*
- Create a power and mute button.
- Create a keyboard movement button.
---
  

Thanks a lot to:
- [kvosbur](https://github.com/kvosbur)
