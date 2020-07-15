from rshell import pyboard

import morse

DEVICE = "/dev/ttyUSB0"
BAUDRATE = 115200
USER = "micro"
PASSWORD = "python"
PIN = {
    "led": 27,
    "servo": 25,
}
RCODE_VALUES = {
    "servo_freq": 50,
    "servo_release": 110,
    "servo_tap": 102,
}  # change these according to your servo and angle


rcode_led = """

from machine import Pin
import time

led = Pin({pin}, Pin.OUT)
led.value(0)

for interval in {flip_intervals}:
    time.sleep(interval / 1000)
    led.value( not led.value() )

led.value(0)

"""
rcode_servo = """

from machine import Pin, PWM
import time

servo = PWM(Pin({pin}), freq={servo_freq}, duty={servo_release})

duty = {servo_release}
time.sleep(0.5)
for interval in {flip_intervals}:
    time.sleep(interval / 1000)
    if duty == {servo_release}:
        duty = {servo_tap}
        servo.duty({servo_tap})
    else:
        duty = {servo_release}
        servo.duty({servo_release})

servo.duty({servo_release})
time.sleep(0.5)
servo.deinit()

"""
rcode = {  # MicroPython code
    "led": rcode_led,
    "servo": rcode_servo,
}


WPM = morse.WPM
FS = morse.FS


def info(device=-1, baudrate=-1, user=-1, password=-1, pins=-1, **rcode_values):
    device = DEVICE if device == -1 else device
    baudrate = BAUDRATE if baudrate == -1 else baudrate
    user = USER if user == -1 else user
    password = PASSWORD if password == -1 else password
    pins = PIN if pins == -1 else pins
    values = RCODE_VALUES.copy()
    values.update(rcode_values)
    print("Pyboard :")
    print(" device             =", device)
    print(" baudrate           =", baudrate)
    print(" user               =", user)
    print(" password           =", password)
    print(" pins               =", pins)
    print(" values             =", values)


def main(
    message,
    wpm=-1,
    fs=-1,
    device=-1,
    baudrate=-1,
    user=-1,
    password=-1,
    pin=-1,
    component="led",
    **rcode_values,
):
    wpm = WPM if wpm == -1 else wpm
    fs = FS if fs == -1 else fs
    device = DEVICE if device == -1 else device
    baudrate = BAUDRATE if baudrate == -1 else baudrate
    user = USER if user == -1 else user
    password = PASSWORD if password == -1 else password
    pin = PIN[component] if pin == -1 else pin
    values = RCODE_VALUES.copy()
    values.update(rcode_values)
    values["pin"] = pin

    code = morse.stringToMorse(message)
    flip_intervals = morse.morseToFlipIntervals(code, wpm, fs)
    values["flip_intervals"] = flip_intervals.tolist()
    pyb = pyboard.Pyboard(device=device, baudrate=baudrate, user=user, password=password)
    pyb.enter_raw_repl()
    pyb.exec(rcode[component].format(**values))
    pyb.exit_raw_repl()
    pyb.close()
