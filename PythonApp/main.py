'''
Made by Aayush Pokharel

Project Started on: Feb 16, 2020

https://github.com/Aayush9029

'''

from pyautogui import press, hotkey
from flask import Flask, render_template, request
from time import sleep
import socket
import qrcode
from PIL import Image
import sys
from os import uname


# Fall back for unix devices. If you have fix to this issue please sumbit a pull request.
macKeys = {
    'playpause'  : 'space',
    'volumeup'   : 'up', 
    'prevtrack'  : 'left',
    'volumedown' : 'down',
    'nexttrack'  : 'right',
    'volumemute' : 'm'
}

def find_os():
    '''
    Returns OS info.
    '''
    os_name = ''
    if sys.platform == 'win32':
        os_name = "windows"
    else:
        if uname()[0] == 'Darwin':
            os_name = "mac"
        elif uname()[0] == 'Linux':
            os_name = "linux"
        else:
            os_name = "not_windows"
    return os_name
# this enables / disables macOs fallback.


def find_ip():
    '''
    Returns local IP address of the machine.
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # this sees if device is connected to internet
    ip = s.getsockname()[0]
    s.close()
    return ip

# this get's printed if the program occurs a runtime error.
issues = f'''
    Sorry, There seems to be a bug.
    Would you mind submitting an issue on the github repo?
    Please include this => {sys.platform} | {find_ip()}
    https://github.com/Aayush9029/Rifi/issues
    '''

def inialize():
    global changeKeys
    '''
    Initializes ip address, port.
    Asks user if they want to view qr code.
    Checks if OS  is recognized or not.
    '''
    ip = find_ip()
    port_num = 8000

    if find_os() == 'mac':
        changeKeys = True
    elif find_os() == 'not_windows':
        print(issues)
        
    ask = input("do you want to see the qr Code? ")

    if ask.lower() == 'y' or ask.lower() == 'yes':
        qrCode = qrcode.make(f"http://{ip}:{port_num}")
        qrCode.show()
    else:
        print('-' * 50 + '\n' * 5)
        print(f"Type this in Apple watch app =>  {ip}:{port_num}")
        print('\n' * 5 + '-' * 50)

    print("\n\nminimize this application\n\n")
    return (ip, port_num)


ip, port_num = inialize()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/press")
def do_press():
    key = request.args.get("key", "None")
    success = True
    
    try:
        if changeKeys and key != "power" and key in macKeys:
            press(macKeys[key])
        elif key == 'power' and changeKeys:
            hotkey('command', 'q')
        elif key == 'power':
            hotkey('alt', 'f4')
        else:
            press(key)
    except:
        success = False

    print("_________>   ",changeKeys, key)

    return {"press": success}


# change the port to any number 8000 to 65534
app.run(host="0.0.0.0", port=port_num)
