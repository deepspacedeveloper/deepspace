'''Events
'''
from deepspace.math2d import Point2d
from deepspace.behaviour import LinearMovement

class AbstractEvent(object):
    'astract event'
    def __init__(self):
        super(AbstractEvent, self).__init__()

    def execute(self):
        'execute event'
        pass


class ClientMouseEvent(AbstractEvent):
    'client press the mouse'
    def __init__(self):
        super(ClientMouseEvent, self).__init__()
        self.mouse_world_position       = None
        self.client_visible_character   = None
        self.remote_client              = None

    def attach(self, mouse_world_position, client_visible_character, remote_client):
        'attach to objects for deffered execution'
        self.mouse_world_position       = mouse_world_position
        self.client_visible_character   = client_visible_character
        self.remote_client              = remote_client
        
    def execute(self):
        super(ClientMouseEvent, self).execute()

        self.client_visible_character.remove_all_behaviours()
       
        point_from = Point2d()
        point_from.set_xy(self.client_visible_character.world_position.x, self.client_visible_character.world_position.y) 
        
        linear_movement = LinearMovement(point_from, self.mouse_world_position, self.client_visible_character.max_speed) 
        self.client_visible_character.add_behaviour(linear_movement)
        
        self.remote_client.line_speed.set_dxdy(self.client_visible_character.speed_x, self.client_visible_character.speed_y)
        self.remote_client.need_refresh_visible_objects = True
        