"""
Adapted from pysine module.

On fedora, you need to install portaudio-devel: dnf install portaudio-devel

"""


import threading
from pyaudio import PyAudio
import numpy as np



class PySine:
    BITRATE = 96000

    def __init__(self):
        self.pyaudio = PyAudio()
        self.stream = self.pyaudio.open(
            format=self.pyaudio.get_format_from_width(1),
            channels=1,
            rate=self.BITRATE,
            output=True
        )

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()

    def sine(self, frequency=440.0, duration=1.0):
        points = int(self.BITRATE * duration)
        times = np.linspace(0, duration, points, endpoint=False)
        data = np.array((np.sin(times*frequency*2*np.pi) + 1.0)*127.5, dtype=np.int8).tostring()
        self.stream.write(data)


def play(frequency=440.0, duration=0.07, *, cls=PySine(), inthread:bool=False):
    call = lambda: cls.sine(frequency=frequency, duration=duration)
    if inthread:
        if play.thread:
            play.thread.join()
        play.thread = threading.Thread(target=call)
        play.thread.start()
    else:
        call()
play.thread = None


if __name__ == "__main__":
    play(440)
