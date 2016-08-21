"""Characters classes
"""
import uuid
from deepspace.math2d import Point2d

class Character(object):
    """Base Character class
    """
    def __init__(self, name=None, x=0, y=0, scale=1):
        self.uuid = ""
        self.uuid = uuid.uuid4().hex
        
        self.speed_x = 0.0
        self.speed_y = 0.0
    
        self.behaviours = []
    
        self.world_position = Point2d()
        self.world_position.set_xy(x, y)

        self.scale = scale
        self.client_should_be_refreshed = False

        print("self.uuid",self.uuid)
        print("__init__=",x,y)

    def update(self, elapsed_time):
        """update character state
        """
        print("update")
        print("self.uuid",self.uuid)
        print("world_position.x",self.world_position.x)
        
        for behaviour in self.behaviours:
            if behaviour.is_done():
                behaviour.detach()
                self.behaviours.remove(behaviour)
                self.client_should_be_refreshed = True
            else:
                behaviour.animate(elapsed_time)


    def add_behaviour(self, behaviour):
        """add behaviour
        """
        behaviour.attach(self)
        self.behaviours.append(behaviour)

        self.client_should_be_refreshed = True


