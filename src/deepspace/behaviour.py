""" Behaviour classes
"""
import math
from deepspace.math2d import Point2d

class AbstractAnimator(object):
    """Base class for Command
    """
    def __init__(self):
        super(AbstractAnimator, self).__init__()
        
        self.character     = None


    def attach_to_character(self, character):
        """ attach_to_character to character
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


class LinearMovementAnimator(AbstractAnimator):
    """2d linear movement animator
    """
    def __init__(self, point_from, point_to, speed):
        super(LinearMovementAnimator, self).__init__()
       
        self.point_from = Point2d()
        self.point_from.set_xy(point_from.x, point_from.y)
        
        self.point_to   = Point2d()
        self.point_to.set_xy(point_to.x, point_to.y)
        self.speed      = speed
        self.speed_x         = 0.0
        self.speed_y         = 0.0
        self.animation_elapsed_time = 0.0


    def attach_to_character(self, character):
        """ attach_to_character and init params
        """
        super(LinearMovementAnimator, self).attach_to_character(character)

        total_length = math.sqrt(math.pow(self.point_to.x - self.point_from.x, 2)+
                                 math.pow(self.point_to.y - self.point_from.y, 2))
        
        if self.speed != 0 and total_length !=0:
            total_time = total_length/self.speed
            
            self.speed_x = (self.point_to.x - self.point_from.x)/total_time
            self.speed_y = (self.point_to.y - self.point_from.y)/total_time
            
            self.character.speed_x += self.speed_x
            self.character.speed_y += self.speed_y 
            
            self.character.world_position.x = self.point_from.x
            self.character.world_position.y = self.point_from.y
    
            self.animation_elapsed_time = total_time
        else:
            self.speed_x = 0
            self.speed_y = 0
            
            self.character.world_position.x = self.point_from.x
            self.character.world_position.y = self.point_from.y
    
            self.animation_elapsed_time = 0


    def animate(self, elapsed_time):
        """Animate character
        """
        delta_x = self.speed_x * elapsed_time
        delta_y = self.speed_y * elapsed_time

        self.character.world_position.x += delta_x
        self.character.world_position.y += delta_y

        if self.point_from.x <  self.point_to.x:
            if self.character.world_position.x >= self.point_to.x:
                self.character.world_position.x = self.point_to.x

        if self.point_from.x >  self.point_to.x:
            if self.character.world_position.x <= self.point_to.x:
                self.character.world_position.x = self.point_to.x

        if self.point_from.y <  self.point_to.y:
            if self.character.world_position.y >= self.point_to.y:
                self.character.world_position.y = self.point_to.y

        if self.point_from.y >  self.point_to.y:
            if self.character.world_position.y <= self.point_to.y:
                self.character.world_position.y = self.point_to.y

        self.animation_elapsed_time -= elapsed_time
        
        if self.animation_elapsed_time < 0:
            self.animation_elapsed_time = 0 


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
        