"""
Converts text to morse code signals

funny_morse:
 | __init__.py                           :
 | __main__.py    # CLI                  :
 | morseTable.py  # char -> morse code   :
 | morse.py       # main                 :
 | play.py        # audio, audio_file    :
 | show.py        # window (tkinter)     :
 | key.py         # keyboard leds        :
 | pyboard.py     # LED, Servo           :
 | parallel.py    # For parallel modes   :
 `````````````````````````````````````````
Tested on:
 | python         v3.8.2-final           :
 | numpy          1.18.4                 :
 | sounddevice    0.3.15                 :
 | wavio          0.0.4                  :
 | pynput         1.6.8                  :
 | rshell         0.0.28                 :
 $ ESP32          MicroPython idf3 v1.12 :
 `````````````````````````````````````````
"""


__title__ = "funny-morse"
__author__ = "Naveen S R"
__license__ = "MIT"
__copyright__ = "Copyright 2020 Naveen S R"

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import morse
import play, show, key, pyboard
from parallel import Parallel

sys.path.pop(0)

code = morse.stringToMorse


def audio(message, wpm=-1, fs=-1, sps=-1, freq=-1):
    """ To play morse code audio signal for message
    Args:
        message: Message to convert
        wpm: Words per minute
        fs: Farnsworth speed
        sps: Samples per second
        freq: Frequency of audio signal
    """
    wpm = morse.WPM if wpm == -1 else wpm
    fs = morse.FS if fs == -1 else fs
    play.main(message, wpm, fs, sps, freq)


def audio_file(filename, message, wpm=-1, fs=-1, sps=-1, freq=-1):
    """ To save morse code audio file for message
    Args:
        filename: filepath for audio output file
        message: Message to convert
        wpm: Words per minute
        fs: Farnsworth speed
        sps: Samples per second
        freq: Frequency of audio signal
    """
    wpm = morse.WPM if wpm == -1 else wpm
    fs = morse.FS if fs == -1 else fs
    play.main(message, wpm, fs, sps, freq, out_file=filename)


def window(message, wpm=-1, fs=-1, title=-1, geometry=-1):
    """ To show morse code signal in a window for message
    Args:
        message: Message to convert
        wpm: Words per minute
        fs: Farnsworth speed
        title: Title for window
        geometry: Geometry for window (format: widthxheight+x+y)
    """
    wpm = morse.WPM if wpm == -1 else wpm
    fs = morse.FS if fs == -1 else fs
    show.main(message, wpm, fs, title, geometry)


def caps_lock(message, wpm=-1, fs=-1):
    """ To show message as morse code by blinking caps lock indicator
    Args:
        message: Message to convert
        wpm: Words per minute
        fs: Farnsworth speed
    """
    wpm = morse.WPM if wpm == -1 else wpm
    fs = morse.FS if fs == -1 else fs
    key.main(message, wpm, fs, key="caps")


def num_lock(message, wpm=-1, fs=-1):
    """ To show message as morse code by blinking num lock indicator
    Args:
        message: Message to convert
        wpm: Words per minute
        fs: Farnsworth speed
    """
    wpm = morse.WPM if wpm == -1 else wpm
    fs = morse.FS if fs == -1 else fs
    key.main(message, wpm, fs, key="num")


def scroll_lock(message, wpm=-1, fs=-1):
    """ To show message as morse code by blinking scroll lock indicator
    Args:
        message: Message to convert
        wpm: Words per minute
        fs: Farnsworth speed
    """
    wpm = morse.WPM if wpm == -1 else wpm
    fs = morse.FS if fs == -1 else fs
    key.main(message, wpm, fs, key="scroll")


def led(message, wpm=-1, fs=-1, device=-1, baudrate=-1, user=-1, password=-1, pin=-1):
    """ To show message as morse code by blinking LED on Microcontroller with MicroPython
    Args:
        message: Message to convert
        wpm: Words per minute
        fs: Farnsworth speed
        device: pyboard port or ip ...
        baudrate: baudrate for communication
        user: username for connecting to pyboard
        password: password for connecting to pyboard
        pin: pin number where component is connected
    """
    wpm = morse.WPM if wpm == -1 else wpm
    fs = morse.FS if fs == -1 else fs
    pyboard.main(message, wpm, fs, device, baudrate, user, password, pin, component="led")


def servo(
    message, wpm=-1, fs=-1, device=-1, baudrate=-1, user=-1, password=-1, pin=-1, **rcode_values
):
    """ To show message as morse code by blinking LED on Microcontroller with MicroPython
    Args:
        message: Message to convert
        wpm: Words per minute
        fs: Farnsworth speed
        device: pyboard port or ip ...
        baudrate: baudrate for communication
        user: username for connecting to pyboard
        password: password for connecting to pyboard
        pin: pin number where component is connected
        **rcode_values: to change values(pyboard.RCODE_VALUES) in rcode_servo
    """
    wpm = morse.WPM if wpm == -1 else wpm
    fs = morse.FS if fs == -1 else fs
    pyboard.main(
        message, wpm, fs, device, baudrate, user, password, pin, component="servo", **rcode_values
    )
