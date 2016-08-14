"""Characters classes
"""

class Character():
    """Base Character class
    """
    def __init__(self, name=None, x=0, y=0, scale=1):
        self._position_x = x
        self._position_y = y
        self.scale = scale
        self._behaviours = []

        if name is None:
            self._name = "noname"
        else:
            self._name = name

    def get_name(self):
        """return name of the character
        """
        return self._name


    def set_name(self, name):
        """set name for the object
        """
        self._name = name


    def set_x(self, position_x):
        """setter for position_x
        """
        self._position_x = position_x


    def set_y(self, position_y):
        """setter for position_y
        """
        self._position_y = position_y


    def get_x(self):
        """return position_x
        """
        return self._position_x


    def get_y(self):
        """return position_y
        """
        return self._position_y


    def update(self):
        """update character state
        """
        for behaviour in self._behaviours:
            if behaviour.is_done():
                self._behaviours.remove(behaviour)
            else:
                behaviour.animate()


    def add_behaviour(self, behaviour):
        """add behaviour
        """
        behaviour.attach(self)
        self._behaviours.append(behaviour)


