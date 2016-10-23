"""Characters classes
"""
import uuid
from deepspace.math2d import Point2d

class Character(object):
    """Base Character class
    """
    def __init__(self, name=None, x=0, y=0, scale=1):
        super(Character, self).__init__()
        if name:
            self.uuid = name
        else:
            self.uuid = uuid.uuid4().hex
        
        self.speed_x = 0.0
        self.speed_y = 0.0
        
        self.max_speed = 0
    
        self.behaviours = []
    
        self.world_position = Point2d()
        self.world_position.set_xy(x, y)

        self.scale = scale
        self.client_should_be_refreshed = False


    def update(self, elapsed_time):
        """update character state
        """
        for behaviour in self.behaviours:
            if not behaviour.is_done():
                behaviour.animate(elapsed_time)

            if behaviour.is_done():
                behaviour.detach()
                self.behaviours.remove(behaviour)
                self.client_should_be_refreshed = True

        
    def add_behaviour(self, behaviour):
        """add behaviour
        """
        behaviour.attach_to_character(self)
        self.behaviours.append(behaviour)

        self.client_should_be_refreshed = True
        

    def remove_all_behaviours(self):
        'remove all animators'
        for behaviour in self.behaviours:
            behaviour.detach()
            self.behaviours.remove(behaviour)
        
        self.client_should_be_refreshed = True
        

