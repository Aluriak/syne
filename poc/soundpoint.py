"""Definition of soundpoint, based on synepoint.

"""
import random
import playsound
import time
import musthe  # theoretical music
from synepoint import Synepoint
from utils import right_left_walk


class Soundpoint(metaclass=Synepoint):
    """A soundpoint associate to one breakpoint a tone on a scale.

    """

    def new_point(self):
        "Return a new note/frequency"
        new_freq = next(self.options['notes'])
        return new_freq.scientific_notation(), new_freq.frequency()

    def on_point(self, name:str, freq:float):
        "Action to do when encountering a point with given payload"
        if self.options['show_notes']:
            print(self.options['show_notes_template'].format(name, freq))
        time_between_notes = self.options['time_between_notes']
        inthread = time_between_notes != 0
        playsound.play(freq, self.options['duration'], inthread=inthread)
        if time_between_notes is not None and time_between_notes > 0:
            time.sleep(time_between_notes)

    def set_opt(self, scale_root:str='B2', scale_type:str='major',
                duration:float=0.08, show_notes:bool=False,
                randomize:bool=False, time_between_notes:float=None,
                show_notes_template:str='{name} ({freq})'):
        "Populate config based on given args"
        scale_is_all = {None, 'all', 'ALL'}
        if scale_root in scale_is_all or scale_type in scale_is_all:
            # use all available notes
            scale = musthe.Note.all(min_octave=2, max_octave=6)  # not too high, it hurts
        else:  # valid input: use given scale
            scale = musthe.Scale(scale_root, scale_type)
        if randomize:
            scale = list(scale)
            random.shuffle(scale)
        else:  # sort by making very different notes succeeding each others
            scale = list(scale)
            scale = tuple(scale[idx] for idx in right_left_walk(len(scale)))
        scale = tuple(scale)
        return {
            'scale': scale,
            'notes': iter(scale),
            'duration': float(duration),
            'show_notes': bool(show_notes),
            'time_between_notes': time_between_notes,
            'show_notes_template': str(show_notes_template),
        }





if __name__ == '__main__':
    from synepoint import soundpoint
    soundpoint.set_opt(scale_root=None, time_between_notes=0.18)
    def myfunc():
        print('hello', end='', flush=True)
        soundpoint()
        print('world', end='', flush=True)
        soundpoint(duration=.5)
        print('!')
        soundpoint()
    # you should get two times the same three notes, with the middle one shorter.
    myfunc()
    myfunc()
