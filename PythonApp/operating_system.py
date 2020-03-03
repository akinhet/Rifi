import abc
from pyautogui import press, hotkey
import sys
import os

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
        try:
            if action != "power":
                press(action)
            else:
                hotkey('alt', 'f4')
            return True
        except Exception:
            return False

    @property
    def name(self):
        return "WINDOWS"


class MAC(OS):

    def do_action(self, action):
        macKeys = {
            'playpause': 'space',
            'volumeup': 'up',
            'prevtrack': 'left',
            'volumedown': 'down',
            'nexttrack': 'right',
            'volumemute': 'm'
        }
        try:
            if action != "power":
                press(macKeys[action])
            else:
                hotkey('command', 'q')
            return True
        except Exception:
            return False

    @property
    def name(self):
        return "MAC"


class Linux(OS):

    def do_action(self, action):
        try:
            if action != "power":
                press(action)
            else:
                hotkey('alt', 'f4')
            return True
        except Exception:
            return False

    @property
    def name(self):
        return "LINUX"


