'''Singleton pattern
'''


class Borg(object):
    'Borg pattern for Singleton implementation'
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class Singleton(Borg):
    'Singleton pattern implementation'

    def __init__(self):
        Borg.__init__(self)
