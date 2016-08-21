""" Behaviour classes
"""
import math

class BaseBehaviour(object):
    """Base class for Command
    """
    def __init__(self):
        super(BaseBehaviour, self).__init__()
        
        self.character     = None


    def attach(self, character):
        """ attach to character
        """
        self.character     = character


    def animate(self, elapsed_time):
        """Animate character
        """
        pass

    def is_done(self):
        """Return True if behaviour is finished and should be deleted
        """
        pass

    def detach(self):
        'detach from object'
        pass


class LinearMovement(BaseBehaviour):
    """2d linear movement animator
    """
    def __init__(self, point_from, point_to, speed):
        super(LinearMovement, self).__init__()
       
        self.point_from = point_from
        self.point_to   = point_to
        self.speed      = speed
        self.speed_x         = 0.0
        self.speed_y         = 0.0
        self.animation_elapsed_time = 0.0


    def attach(self, character):
        """ attach and init params
        """
        super(LinearMovement, self).attach(character)

        total_length = math.sqrt(math.pow(self.point_to.x - self.point_from.x, 2)+
                                 math.pow(self.point_to.y - self.point_from.y, 2))
        
        total_time = total_length/self.speed
        
        self.speed_x = (self.point_to.x - self.point_from.x)/total_time
        self.speed_y = (self.point_to.y - self.point_from.y)/total_time
        
        self.character.speed_x += self.speed_x
        self.character.speed_y += self.speed_y 

        self.animation_elapsed_time = total_time

    def animate(self, elapsed_time):
        """Animate character
        """
        delta_x = self.speed_x * elapsed_time
        delta_y = self.speed_y * elapsed_time

        self.character.world_position.x += delta_x
        self.character.world_position.y += delta_y

        self.animation_elapsed_time -= elapsed_time


    def is_done(self):
        """Return True if animation is finished and should be deleted
        """
        if self.animation_elapsed_time <= 0:
            return True
        return False


    def detach(self):
        'detach from object'
        self.character.speed_x -= self.speed_x
        self.character.speed_y -= self.speed_y 
        