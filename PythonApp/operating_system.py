import abc
from pyautogui import press, hotkey
import sys
import os
import subprocess

class OS:

    NAME = "OS"

    @abc.abstractmethod
    def do_action(self, action) -> bool:
        '''
        This method is meant to complete any given action for the corresponding os
        action - string of action to take
        '''

    @abc.abstractmethod
    def name(self):
        '''
        This returns the name of the OS in question
        '''

    @staticmethod
    def get_os():
        if sys.platform == 'win32':
            return Windows()
        else:
            if os.uname()[0] == 'Darwin':
                return MAC()
            elif os.uname()[0] == 'Linux':
                return Linux()
            else:
                raise Exception("Unkown OS " + os.uname()[0])


class Windows(OS):

    def do_action(self, action):

        windowKeys = {            
        'playpause' : 'playpause',
        'volumeup' : 'volumeup',
        'prevtrack' : 'prevtrack',
        'volumedown': 'volumedown',
        'nexttrack' : 'nexttrack',
        'volumemute' : 'volumemute',
        'down': 'down',
        'up': 'up',
        'right':'right',
        'left':'left',
        'space':'space' 
        }

        try:
            if action == 'power':
                hotkey('alt', 'f4')
            elif action in windowKeys:
                press(windowKeys[action])
            else:
                pass
                # print("unknown button") # prevents people from injecting keys in url ^ .

            return True
        except Exception:
            return False

    @property
    def name(self):
        return "WINDOWS"


class MAC(OS):

    isMuted = False
    currentVolume = 5

    def currentVolumeInfo(self):
        cmd = "osascript -e 'output volume of (get volume settings)'"
        s = subprocess.run(cmd, shell=True, capture_output=True)
        print(s)
        self.currentVolume = int(s.stdout.decode().split()[0]) // 10  # mapping value  of 0-100 to 0-10.


    def controllVolume(self, vc):

        if self.currentVolume > 7 or self.currentVolume < 1:   # adding restrections (apple scripts lets one map from 0 to 7)
            self.currentVolume = 0 if self.currentVolume < 1 else 7

        if vc == 'volumedown':
            self.currentVolume -= 1

        if vc == 'volumeup':
            self.currentVolume += 1
            
        os.system(f"osascript -e 'set volume {self.currentVolume}'")
        

    def muteMac(self): # Mutes and unmutes fix.

        if not self.isMuted:
            os.system("osascript -e 'set volume output muted true'")
            self.isMuted = True
        else:
            os.system("osascript -e 'set volume output muted false'")
            self.isMuted = False


    def do_action(self, action):

        # prevents people from injecting keys in url.
        macKeys = { 
            'playpause': 'space',
            'prevtrack': 'left',
            'nexttrack': 'right',
            'down': 'down',
            'up': 'up',
            'right':'right',
            'left':'left',
            'space':'space'     
        }
        try:
            # print("action: ", action)
            if action == 'power':
                hotkey('command', 'q')
            elif action == 'volumemute':
                self.muteMac()
            elif action == 'volumeup' or action == 'volumedown':
                self.controllVolume(action)
            elif action in macKeys:
                press(macKeys[action])
            else:
                # print("unknown button") # prevents people from injecting keys in url ^ .
                pass
            return True
        except Exception:
            return False

    @property
    def name(self):
        return "MAC"


class Linux(OS):

    def do_action(self, action):
        linuxKeys = {            
            'playpause' : 'space',
            'volumeup' : 'up',
            'prevtrack' : 'left',
            'volumedown': 'down',
            'nexttrack' : 'right',
            'volumemute' : 'm',
            'down': 'down',
            'up': 'up',
            'right':'right',
            'left':'left',
            'space':'space'
        }
        try:
            if action == 'power':
                hotkey('alt', 'f4')
            elif action in linuxKeys:
                press(linuxKeys[action])
            else:
                # print("unknown button") # prevents people from injecting keys in url ^ .
                pass

            return True
        except Exception:
            return False

    @property
    def name(self):
        return "LINUX"


'''need to fix linux media controls'''
