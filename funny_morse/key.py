import time
from pynput import keyboard

import morse

WPM = morse.WPM
FS = morse.FS


def info():
    print("Keyboard :")
    print(" None")


def main(message, wpm=-1, fs=-1, key="caps"):
    wpm = WPM if wpm == -1 else wpm
    fs = FS if fs == -1 else fs
    code = morse.stringToMorse(message)
    flip_intervals = morse.morseToFlipIntervals(code, wpm, fs)
    Keys(flip_intervals, key)


class Keys(keyboard.Controller):
    def __init__(self, flip_intervals, key="caps"):
        self.flip_intervals = flip_intervals
        self.previous = False
        if key == "num":
            self.key = keyboard.Key.num_lock
        elif key == "scroll":
            self.key = keyboard.Key.scroll_lock
        else:
            self.key = keyboard.Key.caps_lock
        super().__init__()
        self.update()

    def flip(self):
        self.press(self.key)
        self.release(self.key)

    def update(self):
        for sleep in self.flip_intervals:
            time.sleep(sleep / 1000)
            self.flip()
