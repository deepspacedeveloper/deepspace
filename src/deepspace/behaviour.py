""" Behaviour classes
"""


class BaseBehaviour(object):
    """Base class for Command
    """
    def __init__(self):
        object.__init__(self)
        self._character     = None


    def attach(self, character):
        """ attach to character
        """
        self._character     = character


    def animate(self):
        """Animate character
        """
        pass

    def is_done(self):
        """Return True if behaviour is finished and should be deleted
        """
        pass
