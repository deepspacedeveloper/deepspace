'''Singleton pattern
'''


class Singleton(object):
    'Singleton pattern implementation'
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance
