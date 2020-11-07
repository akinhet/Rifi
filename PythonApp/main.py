'''
Made by Aayush Pokharel
Project Started on: Feb 16, 2020
https://github.com/Aayush9029
'''

import socket
from flask import Flask, render_template, request
import qrcode_terminal
import operating_system


def find_ip():
    '''
    Returns local IP address of the machine.
    '''
    socket_lib = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # this sees if device is connected to internet
    socket_lib.connect(("8.8.8.8", 80))
    ip_address = socket_lib.getsockname()[0]
    socket_lib.close()
    return ip_address


myOS = operating_system.OS.get_os()

issues = f'''
    Sorry, There seems to be a bug.
    Would you mind submitting an issue on the github repo?
    Please include this => {myOS.name} | {find_ip()}
    https://github.com/Aayush9029/Rifi/issues
    '''


def inialize():
    '''
    Initializes ip address, port.
    Asks user if they want to view qr code.
    Checks if OS  is recognized or not.
    '''
    ip_addr = find_ip()
    port_number = 8000

    ask = input("do you want to see the qr Code? ")

    if ask.lower() == 'y' or ask.lower() == 'yes':
        qrcode_terminal.draw(f'http://{ip_addr}:{port_number}')
    else:
        print('-' * 50 + '\n' * 5)
        print(f"Type this in Apple watch app =>  {ip_addr}:{port_number}")
        print('\n' * 5 + '-' * 50)

    print("\n\nminimize this application\n\n")
    print("Your ip:", ip_addr)
    print("Port:", port_number)
    print("OS:", myOS.name)

    return (ip_addr, port_number)


ip, port_num = inialize()

app = Flask(__name__)


VOLUMESLIDERSTEP = 0.05


@app.route("/")
def index():
    '''
    Serves index page on /
    '''
    return render_template(
        "index.html", volume=myOS.get_volume(), volumeSliderStep=VOLUMESLIDERSTEP)


@app.route("/press")
def do_press():
    '''
    Listens on /press for key presses.
    '''
    key = request.args.get("key", None)
    volume = request.args.get("volume", None)
    success = myOS.do_action(key, volume)

    return {"press": success}


@app.route("/getvolume")
def get_volume():
    '''
    returns for volume value of the system. almost an 'api'
    '''
    return{"volume": myOS.get_volume()}


# change the port to any number 8000 to 65534
app.run(host="0.0.0.0", port=port_num)
