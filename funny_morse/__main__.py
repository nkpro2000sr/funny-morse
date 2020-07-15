#!/usr/bin/env python3

import time
import sounddevice as sd
import numpy as np

import morse
import play, show, key, pyboard
import parallel


def info(args):
    if args.play or args.filename:
        play.info()
    if args.window:
        show.info()
    if args.capsL or args.numL or args.scrollL:
        key.info()
    if args.led or args.servo:
        pyboard.info()
    if args.modes:
        parallel.info(args.modes)


def main(args, message, wpm, fs):
    print(morse.stringToMorse(message))
    if args.play:
        play.main(message, wpm, fs)
    if args.filename:
        play.main(message, wpm, fs, out_file=args.filename)
    if args.window:
        show.main(message, wpm, fs)
    if args.capsL:
        key.main(message, wpm, fs, key="caps")
    if args.numL:
        key.main(message, wpm, fs, key="num")
    if args.scrollL:
        key.main(message, wpm, fs, key="scroll")
    if args.led:
        pyboard.main(message, wpm, fs, component="led")
    if args.servo:
        pyboard.main(message, wpm, fs, component="servo")
    if args.modes:
        parallel.Parallel(message, wpm, fs, modes=args.modes).join()


if __name__ == "__main__":
    import sys, argparse

    parser = argparse.ArgumentParser(description="Convert text to morse code signals ;)")
    parser.add_argument("--wpm", type=float, default=-1, help="Words per minute")
    parser.add_argument("--fs", type=float, default=-1, help="Farnsworth speed")
    parser.add_argument("message", nargs="*", help="Text to translate or blank to take from stdin")
    parser.add_argument("-i", action="store_true", help="For interactive convertion")

    parser.add_argument("-p", "--play", action="store_true", help="To play audio signal")
    parser.add_argument("-a", "--audio", dest="filename", type=str, help="To save audio signal")
    parser.add_argument("-w", "--window", action="store_true", help="To show on a window")
    parser.add_argument(
        "-c", "--capsL", action="store_true", help="To show on caps lock indicator"
    )
    parser.add_argument("-n", "--numL", action="store_true", help="To show on num lock indicator")
    parser.add_argument(
        "-s", "--scrollL", action="store_true", help="To show on scroll lock indicator",
    )
    parser.add_argument(
        "-l",
        "--led",
        action="store_true",
        help="To show on LED (required Microcontroller with MicroPython)",
    )
    parser.add_argument(
        "-m",
        "--servo",
        action="store_true",
        help="To tap using servo motor (required Microcontroller with MicroPython)",
    )

    parser.add_argument("-P", "--parallel", dest="modes", nargs="*", help="For parallel modes")

    args = parser.parse_args()
    morse.info(args.wpm, args.fs)
    info(args)

    if len(args.message) > 0:
        message = " ".join(args.message)
        main(args, message, args.wpm, args.fs)
    elif args.i:
        try:
            while True:
                message = input()
                main(args, message, args.wpm, args.fs)
        except EOFError:
            pass
    else:
        message = sys.stdin.read()
        if not message:
            print("Specify a message through the command line or stdin.")
            message = "Specify a message."
        main(args, message, args.wpm, args.fs)
