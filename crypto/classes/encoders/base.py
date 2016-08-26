
from collections import namedtuple

"""This is more for organization.
Encoder namedtuples include two functions: one for encoding data and another for decoding.
"""

Encoder = namedtuple('Encoder', ('encode', 'decode'))

def do_nothing(value, *args, **kwargs):
    return value

NullEncoder = Encoder(do_nothing, do_nothing)
