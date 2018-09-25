"""Definition of soundpoint, based on synepoint.

"""
import random
import time
import musthe  # theoretical music
from .synepoint import Synepoint
from .utils import right_left_walk
from . import playsound


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

    def set_opt(self, scale:str='B2 major',
                duration:float=0.08, show_notes:bool=False,
                randomize:bool=False, time_between_notes:float=None,
                show_notes_template:str='{name} ({freq})'):
        "Populate config based on given args"
        if scale in {None, 'all', 'ALL'}:
            # use all available notes
            scale = musthe.Note.all(min_octave=2, max_octave=6)  # not too high, it hurts
        else:  # valid input: use given scale
            scale_root, scale_type = scale.split(' ') if ' ' in scale else (scale, 'major')
            scale = musthe.Scale(scale_root.upper(), scale_type.lower())
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
