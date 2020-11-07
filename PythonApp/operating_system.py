import abc
import subprocess
import sys
import os
from pyautogui import press, hotkey

VOLUMESTEP = 4


class OS:
    '''
    Class housing custom functions written for diffrent OS
    accordingly. 
    '''
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
        '''
        Returns OS name
        '''
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
    '''
    Custom functions crafted especially for windows OS
    '''

    def __init__(self):
        '''
        Inline import only used by windows OS users
        '''
        from pycaw.pycaw import AudioUtilities
        self.devices = AudioUtilities.GetSpeakers()
        self.get_current_volume()

    def get_current_volume(self):
        '''
        Inline import only used by windows OS users
        '''
        from pycaw.pycaw import IAudioEndpointVolume
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_control = cast(interface, POINTER(IAudioEndpointVolume))
        self.volume = round(100 * volume_control.GetMasterVolumeLevelScalar())

    def set_volume(self):
        '''
        Inline import only used by windows OS users
        '''
        from pycaw.pycaw import IAudioEndpointVolume
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL

        interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_control = cast(interface, POINTER(IAudioEndpointVolume))
        volume_control.SetMasterVolumeLevelScalar(self.volume / 100, None)

    def do_action(self, action, volume):
        '''
        Function that takes input from JS and executes in python via
        pyautogui
        '''
        window_keys = {
            'playpause': 'playpause',
            'volumeup': 'volumeup',
            'prevtrack': 'prevtrack',
            'volumedown': 'volumedown',
            'nexttrack': 'nexttrack',
            'volumemute': 'volumemute',
            'down': 'down',
            'up': 'up',
            'right': 'right',
            'left': 'left',
            'space': 'space'
        }

        try:
            if action == 'power':
                hotkey('alt', 'f4')
            elif action in window_keys:
                press(window_keys[action])
            elif action == "setvolume":
                self.volume = int(volume)
                self.set_volume()
            else:
                # prevents people from injecting keys in url ^ .
                pass
            self.get_current_volume()
            return True
        except Exception:
            import traceback
            traceback.print_exc()
            return False

    @property
    def name(self):
        '''
        Returns OS name
        '''
        return "WINDOWS"


class MAC(OS):
    '''
    MAC OS Class, with functions crafted for macOS running devices.
    '''
    is_muted = False

    def __init__(self):
        self.current_volume_info()

    def current_volume_info(self):
        osa_command = "osascript -e 'output volume of (get volume settings)'"
        sub_proc = subprocess.run(osa_command, shell=True, capture_output=True)
        self.volume = int(sub_proc.stdout.decode().split()[0])

    def set_volume(self):
        os.system(f"osascript -e 'set volume output volume {self.volume}'")

    def controlVolume(self, volume_control_in):
        '''
        Increases / decreases volume
        '''

        if volume_control_in == 'volumedown':
            self.volume -= VOLUMESTEP

        if volume_control_in == 'volumeup':
            self.volume -= VOLUMESTEP

        self.set_volume()

    def do_media(self, key):
        '''
        Quartz seems to have issues so this feature is disabled for now
        (if you want to enable comment line 208 and uncomment 209)
        '''
        relation = {'playpause': 16, 'prevtrack': 18, 'nexttrack': 17}
        try:
            import Quartz
        except:
            print("please install os specific Quartz library using pip")
            return

        def hid_post_aux_key(key):
            '''
            using QUARTZ to perform system functions in lower level
            '''
            def do_key(down):
                cg_event = Quartz.NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
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
                cg_event_ = cg_event.CGEvent()
                Quartz.CGEventPost(0, cg_event_)

            do_key(True)
            do_key(False)

        hid_post_aux_key(relation[key])

    def mute_mac(self):  # Mutes and unmutes fix.
        '''
        function custom crafted for Mac OS running devices
        which mutes and unmutes volume
        '''
        if not self.is_muted:
            os.system("osascript -e 'set volume output muted true'")
            self.is_muted = True
        else:
            os.system("osascript -e 'set volume output muted false'")
            self.is_muted = False

    def do_action(self, action, volume):

        # prevents people from injecting keys in url.
        mac_keys = {
            'playpause': 'space',
            'prevtrack': 'left',
            'nexttrack': 'right',
            'down': 'down',
            'up': 'up',
            'right': 'right',
            'left': 'left',
            'space': 'space'
        }
        # different_media = ['playpause', 'prevtrack', 'nexttrack']
        different_media = []  # temp fix

        try:
            if action == 'power':
                hotkey('command', 'q')
            elif action == 'volumemute':
                self.mute_mac()
            elif action == 'volumeup' or action == 'volumedown':
                self.controlVolume(action)
            elif action in different_media:
                self.do_media(action)
            elif action in mac_keys:
                press(mac_keys[action])
                print(mac_keys[action])
            elif action == "setvolume":
                self.volume = int(volume)
                self.set_volume()
            else:
                # print("unknown button") # prevents people from injecting keys in url ^ .
                pass
            self.current_volume_info()
            return True
        except:
            return False

    @property
    def name(self):
        return "MAC"


class Linux(OS):

    def __init__(self):
        # an import only used for linux users
        try:
            import pulsectl
        except ImportError:
            print("You must install pulsectl module to run on linux")
            print("Try: pip install pulsectl")
            exit(0)

        self.get_volume()

    def get_volume(self):
        from pulsectl import Pulse
        with Pulse() as pulse:
            for input in pulse.sink_input_list():
                if input.name == 'Spotify':
                    self.spotify = input
                    break

        self.volume = self.spotify.volume.value_flat

    def set_volume(self):
        from pulsectl import Pulse

        with Pulse() as pulse:
            self.spotify.volume.value_flat = self.volume
            pulse.volume_set(self.spotify, self.spotify.volume)

    def do_action(self, action, volume):
        linuxKeys = {
            'playpause': 'XF86AudioPlay',
            'volumeup': 'XF86AudioRaiseVolume',
            'prevtrack': 'XF86AudioPrev',
            'volumedown': 'XF86AudioLowerVolume',
            'nexttrack': 'XF86AudioNext',
            'volumemute': 'XF86AudioMute',
            'down': 'down',
            'up': 'up',
            'right': 'right',
            'left': 'left',
            'space': 'space'
        }

        needCommandLine = ['playpause', "volumeup",
                           "prevtrack", "volumedown", "nexttrack", "volumemute"]

        try:
            if action == 'power':
                hotkey('alt', 'f4')
            elif action in needCommandLine:
                cmd = "xdotool key " + linuxKeys[action]
                os.system(cmd)
            elif action in linuxKeys:
                press(linuxKeys[action])
            elif action == "setvolume":
                self.volume = float(volume)
                # not that this does not bring up interface showing volume change.
                self.set_volume()
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
