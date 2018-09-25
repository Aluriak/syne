"""Definition of the Synepoint metaclass, allowing for further
extension of breakpoints behaviour.

"""

import traceback
import magwitch
from functools import wraps


# @magwitch.on  # TODO: make call method having the exact parameters
class Synepoint:
    """Metaclass for all breakpoints of syne package.

    A synepoint subclass is the representation of a type of synepoint,
    for instance a synepoint that beeps when encountered.
    Subclasses are converted as functions that user can import and use,
    and each call to these functions are identifiable in the class.

    """

    def __new__(cls, clsname, bases, attrs):

        def call_method(self, **kwargs):
            trace = traceback.format_stack()[-2]  # the last one, except this level and the call level of subclass
            h = hash(tuple(trace))
            if h not in self.synepoints:
                self.synepoints[h] = self.new_point()
            # call the function with options changed according to given kwargs
            options = dict(self.options)
            options.update(kwargs)
            self.options, options = options, self.options
            self.on_point(*self.synepoints[h])
            self.options, options = options, self.options  # restore
        def init_method(self):
            self.set_opt()

        attrs['__call__'] = call_method
        attrs['__init__'] = init_method
        attrs['synepoints'] = {}  # map synepoint -> payload data
        attrs['options'] = {}  # map option name -> option default

        # wrap set_opt with the standard assignation of self.options
        attrs['_set_opt'] = attrs['set_opt']
        @wraps(attrs['_set_opt'])
        def set_opt_method(self, **kwargs):
            self.options = self._set_opt(**kwargs)
        attrs['setopt'] = attrs['set_opt'] = set_opt_method

        # finally build the function and the class
        final_cls = type(clsname.title(), bases, attrs)
        globals()[clsname.lower()] = final_cls()  # associate an instance with the function
        return final_cls
