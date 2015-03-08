# -*- coding: utf-8 -*-

import inspect

# __all__ defined by the @public decorator on objects


def public(*args, **kwargs):
    """"Use a decorator to automatically update a module's __all__.

    Usage:

    @public
    def public_function():
        ...

    _private_name = public(public_name=a_value)

    If used to decorate a callable, adds object's __name__ to __all__ of modules where 'public' is executed.
    If given a keyword argument, keyword name is added to module.__all__. Additionally, keyword name & value are added
    to the module.__dict__

    :return: callable or keyword value
    """
    if len(args) + len(kwargs) > 1:
        raise AttributeError("Only 1 argument allowed, got {args}, {kwargs}".format(args=args, kwargs=kwargs))

    if args:
        arg, name = args[0], None
    elif kwargs:
        name, arg = kwargs.popitem()
    else:   # No arguments, return None
        return

    module = []
    stack = inspect.stack()
    for frame_record in stack:
        if 'module' in frame_record[3]:
            module.append(inspect.getmodule(frame_record[0]))
            break

    try:
        module = module.pop()
        _all_ = module.__dict__.setdefault('__all__', [])
    except IndexError:
        # Failed to retrieve the appropriate module
        return arg

    if name is None:
        name = arg.__name__
    else:
        module.__dict__[name] = arg
    if name not in _all_:  # Prevent duplicates if run from an IDE.
        _all_.append(name)
    return arg
public(public)


class Logging_Dict(dict):
    prefix = ''

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        print("%sSetting %s = %s" % (self.prefix, key, value))
        return super().__setitem__(key, value)

    def update(self, *args, **kwargs):
        # print("update(%s, %s)" % (args, kwargs))
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

    def pop(self, k, d=None):
        value = super().pop(k, d)
        print("%spop(%s, %s) returned %s" % (self.prefix, k, d, value))
        return value

    def popitem(self):
        k, v = super().popitem()
        print("%spopitem returned %s, %s" % (self.prefix, k, v))
        return k, v

    def copy(self):
        prefix = "Copy of " + self.prefix
        print("Creating " + prefix)
        d = type(self)(super().copy())
        d.prefix = prefix
        print(prefix, d)
        return d

