""" Behaviour classes
"""


class BaseBehaviour(object):
    """Base class for Command
    """

    def __init__(self, character, time):
        object.__init__()
        self._character = character
        self._start_time = time


    def init(self):
        """ Initialisation
        """
        pass


    def animate(self, current_time):
        """Animate character
        """
        pass
