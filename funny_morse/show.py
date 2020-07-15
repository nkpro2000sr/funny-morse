import tkinter

import morse

TITLE = "funny-morse"
GEOMETRY = ""  # Default

WPM = morse.WPM
FS = morse.FS


def info(title=-1, geometry=-1):
    title = TITLE if title == -1 else title
    geometry = GEOMETRY if geometry == -1 else geometry
    print("Window :")
    print(" Title              =", title)
    print(" Geometry           =", repr(geometry))


def main(message, wpm=-1, fs=-1, title=-1, geometry=-1):
    wpm = WPM if wpm == -1 else wpm
    fs = FS if fs == -1 else fs
    title = TITLE if title == -1 else title
    geometry = GEOMETRY if geometry == -1 else geometry
    code = morse.stringToMorse(message)
    flip_intervals = morse.morseToFlipIntervals(code, wpm, fs)
    window = Window(flip_intervals, title, geometry)
    window.mainloop()


class Window(tkinter.Tk):
    def __init__(self, flip_intervals, title=-1, geometry=-1):
        title = TITLE if title == -1 else title
        geometry = GEOMETRY if geometry == -1 else geometry
        self.flip_intervals = flip_intervals
        self.end = len(flip_intervals)
        self.i = 0
        self.previous = False
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.configure(bg="#000000")
        self.update()

    def flip(self):
        self.configure(bg="#000000" if self.previous else "#ffffff")
        self.previous = not self.previous
        self.i += 1
        self.update()

    def update(self):
        if self.i >= self.end:
            self.destroy()
        else:
            sleep = self.flip_intervals[self.i]
            self.after(sleep, self.flip)
