"""Usage example of syne.soundpoint"""

from syne import soundpoint

soundpoint.set_opt(scale=None, time_between_notes=0.18)

def myfunc():
    print('hello', end='', flush=True)
    soundpoint()
    print('world', end='', flush=True)
    soundpoint(duration=.5)
    print('!')
    soundpoint()

# you should get two times the same three notes, with the middle one longer.
myfunc()
myfunc()
