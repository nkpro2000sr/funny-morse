# Funny Morse

Converts text to morse code signals

## Examples

```python3
from funny_morse import *

print(code("Morse code")) # -- --- .-. ... .   -.-. --- -.. .
```

### Audio
```python3
audio("play") # To play morse code audio signal for message

audio_file("code.wav", "wave file", sps=44100, freq=800) # To save
```

### Window
```python3
window("show", wpm=5, fs=None)
```

### Keyboard Leds
```python3
caps_lock("morse")

num_lock("on")

scroll_lock("indicator")
```

### Pyboard
```python3
led("blink", device="/dev/ttyUSB0")

servo("tap", device="192.168.1.1")
```

### Parallel
```python3
Parallel("try parallel",
         modes=[
            play,        # can use callables
            "window"     # can use modes
         ],
         led={
            "pin" : 2,   # kwargs to led mode
         }
         ).join()
```

## CLI Examples
```
usage: funny_morse [-h] [--wpm WPM] [--fs FS] [-i] [-p] [-a FILENAME] [-w] [-c] [-n] [-s] [-l] [-m] [-P [MODES [MODES ...]]] [message [message ...]]

Convert text to morse code signals ;)

positional arguments:
  message               Text to translate or blank to take from stdin

optional arguments:
  -h, --help                                              show this help message and exit
  --wpm WPM                                               Words per minute
  --fs FS                                                 Farnsworth speed
  -i                                                      For interactive convertion
  -p, --play                                              To play audio signal
  -a FILENAME, --audio FILENAME                           To save audio signal
  -w, --window                                            To show on a window
  -c, --capsL                                             To show on caps lock indicator
  -n, --numL                                              To show on num lock indicator
  -s, --scrollL                                           To show on scroll lock indicator
  -l, --led                                               To show on LED (required Microcontroller with MicroPython)
  -m, --servo                                             To tap using servo motor (required Microcontroller with MicroPython)
  -P [MODES [MODES ...]], --parallel [MODES [MODES ...]]  For parallel modes
```

```bash
python -m funny_morse --wpm 15 --fs 15 -p hello
```
> ```
> Dot width           = 80.0 ms
> Dash width          = 240 ms
> Character space     = 240 ms
> Word space          = 560 ms
> Audio :
>  samples per second = 8000
>  Tone period        = 1.3 ms
> .... . .-.. .-.. ---
> ```

### Parallel
```bash
python -m funny_morse -P p w -- now parallelly play audio and show window
```


## Installation

Installation is available via pip:

```bash
pip install funny-morse # From PYPI

## OR ##

pip install git+https://github.com/nkpro2000sr/funny-morse.git # From github repo
```

## Links
* [PyPi](https://pypi.org/project/funny-morse/)
