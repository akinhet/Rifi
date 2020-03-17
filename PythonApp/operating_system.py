import abc
from pyautogui import press, hotkey
import sys
import os
import subprocess

VolumeStep = 4

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
        from pycaw.pycaw import AudioUtilities

        self.devices = AudioUtilities.GetSpeakers()
        self.get_current_volume()


    def get_current_volume(self):
        from pycaw.pycaw import IAudioEndpointVolume
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
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

            self.get_current_volume()

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
            self.volume -= VolumeStep

        if vc == 'volumeup':
            self.volume -= VolumeStep

        self.set_volume()


    def doMedia(self, key):
        relation = {'playpause': 16, 'prevtrack': 18, 'nexttrack': 17}
        try:
            import Quartz
        except:
            print("please install os specific Quartz library using pip")
            return

        def HIDPostAuxKey(key):
            def doKey(down):
                ev = Quartz.NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
                    NSSystemDefined,  # type
                    (0, 0),  # location
                    0xa00 if down else 0xb00,  # flags
                    0,  # timestamp
                    0,  # window
                    0,  # ctx
                    8,  # subtype
                    (key << 16) | ((0xa if down else 0xb) << 8),  # data1
                    -1  # data2
                )
                cev = ev.CGEvent()
                Quartz.CGEventPost(0, cev)

            doKey(True)
            doKey(False)

        HIDPostAuxKey(relation[key])


        

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
        differentMedia = ['playpause', 'prevtrack', 'nexttrack']
        # need to use this for media keys https://stackoverflow.com/questions/11045814/emulate-media-key-press-on-mac
        try:
            # print("action: ", action)
            if action == 'power':
                hotkey('command', 'q')
            elif action == 'volumemute':
                self.muteMac()
            elif action == 'volumeup' or action == 'volumedown':
                self.controlVolume(action)
            elif action in differentMedia:
                self.doMedia(action)
            elif action in macKeys:
                press(macKeys[action])
            elif action == "setvolume":
                self.volume = int(volume)
                self.set_volume()
            else:
                # print("unknown button") # prevents people from injecting keys in url ^ .
                pass
            self.currentVolumeInfo()
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
            print("try running: sudo apt-get install libasound2-dev")
            print("Followed by: pip install pyalsaaudio")
            exit(0)

        self.get_volume()

    def get_volume(self):
        import alsaaudio
        m = alsaaudio.Mixer()
        self.volume = int(m.getvolume()[0])

    def set_volume(self):
        import alsaaudio
        m = alsaaudio.Mixer()
        m.setvolume(self.volume)

    def do_action(self, action, volume):
        linuxKeys = {            
            'playpause' : 'XF86AudioPlay',
            'volumeup' : 'XF86AudioRaiseVolume',
            'prevtrack' : 'XF86AudioPrev',
            'volumedown': 'XF86AudioLowerVolume',
            'nexttrack' : 'XF86AudioNext',
            'volumemute' : 'XF86AudioMute',
            'down': 'down',
            'up': 'up',
            'right':'right',
            'left':'left',
            'space':'space'
        }

        needCommandLine = ['playpause', "volumeup", "prevtrack", "volumedown", "nexttrack", "volumemute"]

        try:
            if action == 'power':
                hotkey('alt', 'f4')
            elif action in needCommandLine:
                cmd = "xdotool key " + linuxKeys[action]
                os.system(cmd)
            elif action in linuxKeys:
                press(linuxKeys[action])
            elif action == "setvolume":
                self.volume = int(volume)
                self.set_volume()  # not that this does not bring up interface showing volume change.
            else:
                # print("unknown button") # prevents people from injecting keys in url ^ .
                pass
            self.get_volume()

            return True
        except Exception:
            import traceback
            traceback.print_exc()
            return False

    @property
    def name(self):
        return "LINUX"
