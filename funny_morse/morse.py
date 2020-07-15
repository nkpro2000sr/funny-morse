import numpy as np

from morseTable import forwardTable, DOT, DASH, DASH_WIDTH, CHAR_SPACE, WORD_SPACE

WPM = 10
FS = 8


def letterToMorse(letter):
    if letter in forwardTable:
        return forwardTable[letter]
    elif letter.isspace():
        return " "
    else:
        return ""


def stringToMorse(string):
    codeArr = [letterToMorse(l) for l in string.upper()]
    trimmedArr = [code for code in codeArr if code]
    return " ".join(trimmedArr)


def morseToBoolArr(code, sps, wpm, fs=None):
    """ morse code to boolean array
    Args:
        code (str): morse code
        sps: Samples per second
        wpm: Words per minute
        fs: Farnsworth speed
    Returns:
        boolean numpy array
    """
    dps = wpmToDps(wpm)  # dots per second
    baseSampleCount = sps / dps
    samplesPerDot = int(round(baseSampleCount))
    samplesPerDash = int(round(baseSampleCount * DASH_WIDTH))
    samplesBetweenElements = int(round(baseSampleCount))
    farnsworthScale = farnsworthScaleFactor(wpm, fs)
    samplesBetweenLetters = int(round(baseSampleCount * CHAR_SPACE * farnsworthScale))
    samplesBetweenWords = int(round(baseSampleCount * WORD_SPACE * farnsworthScale))

    dotArr = np.ones(samplesPerDot, dtype=np.bool)
    dashArr = np.ones(samplesPerDash, dtype=np.bool)
    eGapArr = np.zeros(samplesBetweenElements, dtype=np.bool)
    cGapArr = np.zeros(samplesBetweenLetters, dtype=np.bool)
    wGapArr = np.zeros(samplesBetweenWords, dtype=np.bool)

    pieces = []
    prevWasSpace = False
    prevWasElement = False
    for c in code:
        if (c == DOT or c == DASH) and prevWasElement:
            pieces.append(eGapArr)
        if c == DOT:
            pieces.append(dotArr)
            prevWasSpace, prevWasElement = False, True
        elif c == DASH:
            pieces.append(dashArr)
            prevWasSpace, prevWasElement = False, True
        else:  # Assume the char is a space otherwise
            if prevWasSpace:
                pieces[-1] = wGapArr
            else:
                pieces.append(cGapArr)
            prevWasSpace, prevWasElement = True, False

    return np.concatenate(pieces)


def morseToFlipIntervals(code, wpm, fs=None):
    """ morse code to flip intervals
    Args:
        code (str): morse code
        wpm: Words per minute
        fs: Farnsworth speed
    Returns:
        numpy array of intervals in milliseconds
    """
    dps = wpmToDps(wpm)  # Dots per second
    mspd = 1000 / dps  # Dot duration in milliseconds
    bool_arr = morseToBoolArr(code, dps, wpm, fs)

    flip_interval = []
    previous = False
    span = 0
    for state in bool_arr:
        if state is not previous:
            flip_interval.append(round(span))
            span = 0
            previous = state
        span += mspd
    flip_interval.append(round(span))

    return np.array(flip_interval, dtype=np.int)


def wpmToDps(wpm):
    """ Words per minute = number of times PARIS can be sent per minute.
      PARIS takes 50 dot lengths to send.  Returns dots per seconds. """
    return wpm * 50 / 60.0


def farnsworthScaleFactor(wpm, fs=None):
    """ Returns the multiple that character and word spacing should be multiplied by. """
    if fs is None:
        return 1  # Standard (not Farnsworth) word spacing
    slowWordInterval = 1.0 / fs  # Minutes per word
    standardWordInterval = 1.0 / wpm
    extraSpace = slowWordInterval - standardWordInterval
    extraSpaceDots = (extraSpace / standardWordInterval) * (
        9 + 10 + 4 * DASH_WIDTH + 4 * CHAR_SPACE + WORD_SPACE
    )
    standardSpaceDots = 4 * CHAR_SPACE + WORD_SPACE  # For the word PARIS
    totalSpaceDots = standardSpaceDots + extraSpaceDots
    scaleFactor = totalSpaceDots / standardSpaceDots
    if scaleFactor < 1:
        return 1
    return scaleFactor


def info(wpm=-1, fs=-1):
    """ To print info (Dot width, Dash width, Character space, Word space)
    Args:
        wpm: Words per minute
        fs: Farnsworth speed
    """
    wpm = WPM if wpm == -1 else wpm
    fs = FS if fs == -1 else fs
    dps = wpmToDps(wpm)  # Dots per second
    mspd = 1000 / dps  # Dot duration in milliseconds
    farnsworthScale = farnsworthScaleFactor(wpm, fs)
    print("Dot width           =", round(mspd, 1), "ms")
    print("Dash width          =", int(round(mspd * DASH_WIDTH)), "ms")
    print("Character space     =", int(round(mspd * CHAR_SPACE * farnsworthScale)), "ms")
    print("Word space          =", int(round(mspd * WORD_SPACE * farnsworthScale)), "ms")
