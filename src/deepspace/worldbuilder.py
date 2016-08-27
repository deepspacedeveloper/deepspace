''' world builders
'''
class WorldBuilder(object):
    'build the world from generator'
    def __init__(self):
        pass
    
    def build_world(self, world, abstract_world_generator):
        'build world from given generator'
        abstract_world_generator.generate_world(world)


class AbstractWorldGenerator(object):
    'abstract world builder'
    def __init__(self):
        pass
    
    def generate_world(self, world):
        'generate world'
        pass
    
    
class TestWorldGenerator(AbstractWorldGenerator):
    'test world builder'
    def __init__(self):
        pass
        
    def generate_world(self, world):
        world.build_character(position_x=1000,position_y=1000,scale = 0.2)
        world.build_character(position_x=1100,position_y=1100,scale = 0.2)
        #world.build_character(position_x=1000,position_y=1100,scale = 0.2)
        #world.build_character(position_x=1100,position_y=1000,scale = 0.2)

        #world.build_character(position_x=1000, position_y=2000, scale = 0.2)
        
        #moving_character = world.build_character(position_x=1000, position_y=2000, scale=0.2)
        
        #point_from  = Point2d()
        #point_from.set_xy(moving_character.world_position.x, moving_character.world_position.y)
        
        #point_to    = Point2d()
        #point_to.set_xy(1300, 2300)
        
        #linear_movement = LinearMovement(point_from, point_to, 20)
        #moving_character.add_behaviour(linear_movement)
        