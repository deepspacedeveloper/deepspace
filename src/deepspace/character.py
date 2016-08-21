"""Characters classes
"""
import uuid
from deepspace.math2d import Point2d

class Character():
    """Base Character class
    """
    world_position = Point2d
    uuid = ""

    def __init__(self, name=None, x=0, y=0, scale=1):
        self.world_position.x = x
        self.world_position.y = y
        self.scale = scale
        self._behaviours = []
        self.changed_since_last_update = False
        self.uuid = uuid.uuid4().hex

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


    def update(self):
        """update character state
        """
        for behaviour in self._behaviours:
            if behaviour.is_done():
                self._behaviours.remove(behaviour)
            else:
                behaviour.animate()

        self.changed_since_last_update = True


    def add_behaviour(self, behaviour):
        """add behaviour
        """
        behaviour.attach(self)
        self._behaviours.append(behaviour)


