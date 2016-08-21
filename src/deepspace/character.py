"""Characters classes
"""
import uuid
from deepspace.math2d import Point2d

class Character():
    """Base Character class
    """
    world_position = Point2d
    uuid = ""
    
    speed_x = 0.0
    speed_y = 0.0

    def __init__(self, name=None, x=0, y=0, scale=1):
        self.world_position.x = x
        self.world_position.y = y
        self.scale = scale
        self._behaviours = []
        self.client_should_be_refreshed = False
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


    def update(self, elapsed_time):
        """update character state
        """
        for behaviour in self._behaviours:
            if behaviour.is_done():
                behaviour.detach()
                self._behaviours.remove(behaviour)
                self.client_should_be_refreshed = True
            else:
                behaviour.animate(elapsed_time)


    def add_behaviour(self, behaviour):
        """add behaviour
        """
        behaviour.attach(self)
        self._behaviours.append(behaviour)

        self.client_should_be_refreshed = True


