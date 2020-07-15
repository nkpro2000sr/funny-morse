import time
import sounddevice as sd
import numpy as np
import wavio

import morse

SPS = 8000
FREQ = 750
WPM = morse.WPM
FS = morse.FS
AUDIO_PADDING = 0.5  # Seconds
CLICK_SMOOTH = 2  # Tone periods


def info(sps=-1, freq=-1):
    sps = SPS if sps == -1 else sps
    freq = FREQ if freq == -1 else freq
    print("Audio :")
    print(" samples per second =", sps)
    print(" Tone period        =", round(1000 / freq, 1), "ms")


def main(message, wpm=-1, fs=-1, sps=-1, freq=-1, out_file=None):
    """ Compute morse code audio from plain text """
    wpm = WPM if wpm == -1 else wpm
    fs = FS if fs == -1 else fs
    sps = SPS if sps == -1 else sps
    freq = FREQ if freq == -1 else freq
    audio = stringToMorseAudio(message, wpm, fs, sps, freq, 0.5)
    audio /= 2
    if out_file:
        wavio.write(out_file, (audio * 2 ** 15).astype(np.int16), sps)
    else:
        playBlock(audio, sps)
        time.sleep(0.1)


def boolArrToSwitchedTone(boolArr, freq, sps, volume=1.0):
    """ Create the tone audio from a bool array representation of morse code. """
    weightLen = int(CLICK_SMOOTH * sps / freq)
    if weightLen % 2 == 0:
        weightLen += 1  # Make sure the weight array is odd length
    smoothingWeights = np.concatenate(
        (np.arange(1, weightLen // 2 + 1), np.arange(weightLen // 2 + 1, 0, -1))
    )
    smoothingWeights = smoothingWeights / np.sum(smoothingWeights)
    numSamplesPadding = int(sps * AUDIO_PADDING) + int((weightLen - 1) / 2)
    padding = np.zeros(numSamplesPadding, dtype=np.bool)
    boolArr = np.concatenate((padding, boolArr, padding)).astype(np.float32)
    if CLICK_SMOOTH <= 0:
        smoothBoolArr = boolArr
    else:
        smoothBoolArr = np.correlate(boolArr, smoothingWeights, "valid")
    numSamples = len(smoothBoolArr)
    x = np.arange(numSamples)
    toneArr = np.sin(x * (freq * 2 * np.pi / sps)) * volume
    toneArr *= smoothBoolArr
    return toneArr


def stringToMorseAudio(message, wpm=-1, fs=-1, sps=-1, freq=-1, volume=1.0):
    wpm = WPM if wpm == -1 else wpm
    fs = FS if fs == -1 else fs
    sps = SPS if sps == -1 else sps
    freq = FREQ if freq == -1 else freq
    message = message.upper()
    code = morse.stringToMorse(message)
    boolArr = morse.morseToBoolArr(code, sps, wpm, fs)
    audio = boolArrToSwitchedTone(boolArr, freq, sps, volume)
    return audio


def play(array, sps=-1):
    sps = SPS if sps == -1 else sps
    sd.play(array.astype(np.float32), sps)


def waitFor(array, sps=-1):
    sps = SPS if sps == -1 else sps
    duration = len(array) / sps
    time.sleep(duration)


def playBlock(array, sps=-1):
    sps = SPS if sps == -1 else sps
    play(array, sps)
    waitFor(array, sps)
