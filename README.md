## **RIFI v1.4**
This is the official repo for Wireless Multimedia controller App/Program "RIFI"

Tested on : MacOS | Windows 10 | Manjaro *Linux*

---

```gdscript
# Checks if player collided with enemy
func _on_Area2D_body_entered(body : Node):
	if !wasHit and !knockedOut and !invincible:
		if (position - body.position).normalized().x > 0:
#			set_deferred("direction", Vector2(1, -1))
			direction = Vector2(1, -1)
#			set_deferred("motion", direction * MAX_SPEED / 2)
			motion = direction * MAX_SPEED / 2
		else:
#			set_deferred("direction", Vector2(-1, -1))
			direction = Vector2(-1, -1)
#			set_deferred("motion", direction * MAX_SPEED / 2)
			motion = direction * MAX_SPEED / 2
#		wasHit = true
		lifes -= 1
		set_deferred("wasHit", true)
		emit_signal("hearts_update", lifes)
```

##  [![Watch OS version](https://img.shields.io/badge/WatchOS-6.1-skyblue?style=flat-square)](https://www.apple.com/ca/watchos/watchos-6/)   [![python 3.8](https://img.shields.io/badge/Python-3.8.1-brightred?style=flat-square)](https://www.python.org/) [![ask me why](https://img.shields.io/badge/Rifi-v1.4-purple?style=flat-square)](http://aayush.wtf) [![Xcode 11](https://img.shields.io/badge/Xcode-11-blue?style=flat-square)](https://www.apple.com/) [![iOS 13](https://img.shields.io/badge/iOS-13-pink?style=flat-square)](https://www.apple.com/ios/)
  Watch Connect and Player View</br>
  <img src="Images/wc.png" width="128" >
  <img src="Images/wp.png" width="128" ></br>
  
  iOS APP and Web Controller View</br>
  
  <img src="Images/ipapp.png" width="256"> <img src="Images/ips.png" width="256"></br>
  Android Web Controller View</br>
  <img src="Images/pps.png" width="256"></br>

---
**Installation**

 git clone [repo](https://github.com/Aayush9029/Rifi.git) or Download .zip/.tar file from the [releases](https://github.com/Aayush9029/Rifi/releases).

 `cd PythonApp`

 `pip install -r requirements.txt`

Complie the watchApp/Remote Controller.xcodeproj and install in apple watch

Or Scan qr code to get acces to web interface.

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



Basically this transforms an Apple Watch or a phone to a virtual remote enabling it to controll multimedia.

Uses:

- While Playing a music in laptop (Play/Pause) (Skip) (Volume up/down) 

- While Watching Movie and keyboard/mouse is a bit too far to reach.

- While playing music to skip tracks and since the keystrokes are configurable they can be use to initiate custom shortcuts.

---
### How to install iOS and watchOS app?

- Clone the repo
- Open xcodeproj file for iOS_Rifi
  - Change the bundle id and team 
  - Connect your iphone and run
- Open xcodeproj file for applewatchApp
  - Connect you iphone and apple watch 
  - Change the bundle id and team
  - Run


*Thanks a lot to*:
- [kvosbur](https://github.com/kvosbur)
