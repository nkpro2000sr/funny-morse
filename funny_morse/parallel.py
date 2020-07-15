from threading import Thread
from functools import partial

import play, show, key, pyboard


def info(modes):
    modes = set(modes)
    if modes & {"play", "p"}:
        play.info()
    if modes & {"window", "w"}:
        show.info()
    if modes & {"capsL", "c", "numL", "n", "scrollL", "s"}:
        key.info()
    if modes & {"led", "l", "servo", "m"}:
        pyboard.info()


class Parallel:
    """ To parallel modes """

    def __init__(self, message, wpm=-1, fs=-1, modes=(), **modes_):
        """
        Args:
            message: Message to convert
            wpm: Words per minute
            fs: Farnsworth speed
            modes (List[Union[str,Callable]]): list of modes or callable to call
            **modes_ (Mapping[str,Any]): mapping of modes to kwargs (for modes)
        """
        self.kwargs = {
            "message": message,
            "wpm": wpm,
            "fs": fs,
        }
        self.threads = []
        for mode in modes:
            if type(mode) is str:
                target = self._get_target(mode)
            else:
                target = mode
            kwargs = dict()
            kwargs.update(self.kwargs)
            thread = Thread(target=target, kwargs=kwargs)
            self.threads.append(thread)
        for mode, kwargs_ in modes_.items():
            target = self._get_target(mode)
            kwargs = dict()
            kwargs.update(self.kwargs)
            kwargs.update(kwargs_)
            thread = Thread(target=target, kwargs=kwargs)
            self.threads.append(thread)

    def _get_target(self, mode):
        if mode in ["play", "p"]:
            return play.main
        if mode in ["window", "w"]:
            return show.main
        if mode in ["capsL", "c"]:
            return partial(key.main, key="caps")
        if mode in ["numL", "n"]:
            return partial(key.main, key="num")
        if mode in ["scrollL", "s"]:
            return partial(key.main, key="scroll")
        if mode in ["led", "l"]:
            return partial(pyboard.main, component="led")
        if mode in ["servo", "m"]:
            return partial(pyboard.main, component="servo")
        raise LookupError("Not a valid mode {}".format(mode))

    def start(self):
        """ to start all threads """
        for thread in self.threads:
            thread.start()

    def wait(self):
        """ to wait for all threads to end """
        for thread in self.threads:
            thread.join()

    def join(self):
        """ to start and wait for all threads to end """
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()
