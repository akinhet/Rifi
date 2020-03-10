import abc
from pyautogui import press, hotkey
import sys
import os
import subprocess

class OS:

    NAME = "OS"
    volume = 0

    @abc.abstractmethod
    def do_action(self, action, volume) -> bool:
        '''
        This method is meant to complete any given action for the corresponding os
        action - string of action to take
        '''

    @abc.abstractmethod
    def name(self):
        '''
        This returns the name of the OS in question
        '''

    @abc.abstractmethod
    def set_volume(self):
        '''
        This returns the name of the OS in question
        '''

    def get_volume(self):
        return self.volume

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

    def __init__(self):
        # an import only used for windows users
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL

        self.devices = AudioUtilities.GetSpeakers()
        interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volumeControl = cast(interface, POINTER(IAudioEndpointVolume))
        self.volume = round(100 * volumeControl.GetMasterVolumeLevelScalar())

    def set_volume(self):
        # an import only used for windows users
        from pycaw.pycaw import IAudioEndpointVolume
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL

        interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volumeControl = cast(interface, POINTER(IAudioEndpointVolume))
        volumeControl.SetMasterVolumeLevelScalar(self.volume / 100, None)

    def do_action(self, action, volume):

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
            elif action == "setvolume":
                self.volume = int(volume)
                self.set_volume()
            else:
                pass
                # print("unknown button") # prevents people from injecting keys in url ^ .

            return True
        except Exception:
            import traceback
            traceback.print_exc()
            return False

    @property
    def name(self):
        return "WINDOWS"


class MAC(OS):

    isMuted = False

    def __init__(self):
        self.currentVolumeInfo()

    def currentVolumeInfo(self):
        cmd = "osascript -e 'output volume of (get volume settings)'"
        s = subprocess.run(cmd, shell=True, capture_output=True)
        print(s)
        self.volume = int(s.stdout.decode().split()[0])

    def set_volume(self):
        # used this url as reference https://osxdaily.com/2007/04/28/change-the-system-volume-from-the-command-line/
        os.system(f"osascript -e 'set volume output volume {self.volume}'")

    def controlVolume(self, vc):
        '''
        # don't think this is necessary anymore
        if self.currentVolume > 7 or self.currentVolume < 1:   # adding restrictions (because of apple scripts err!)
            self.currentVolume = 0 if self.currentVolume < 1 else 7
        '''

        if vc == 'volumedown':
            self.volume -= 4

        if vc == 'volumeup':
            self.volume -= 4

        self.set_volume()

        

    def muteMac(self): # Mutes and unmutes fix.

        if not self.isMuted:
            os.system("osascript -e 'set volume output muted true'")
            self.isMuted = True
        else:
            os.system("osascript -e 'set volume output muted false'")
            self.isMuted = False


    def do_action(self, action, volume):

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
                self.controlVolume(action)
            elif action in macKeys:
                press(macKeys[action])
            elif action == "setvolume":
                self.volume = int(volume)
                self.set_volume()
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

    def __init__(self):
        # an import only used for linux users
        try:
            import alsaaudio
        except ImportError:
            print("You must install alsaaudio module to run on linux")
            print("try running: sudo apt-get install python-alsaaudio")
            exit(0)

        m = alsaaudio.Mixer()
        self.volume = int(m.getvolume()[0])

    def set_volume(self):
        m = alsaaudio.Mixer()
        m.setvolume(self.volume)

    def do_action(self, action, volume):
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
            elif action == "setvolume":
                self.volume = int(volume)
                self.set_volume()
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
