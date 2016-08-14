from wor.robot import Robot


class RobotWorld:
    
    def __init__(self):
        self._robot_counter = 0
        self._robot_by_name = {}
        self._all_robots = []
    
    
    def __iter__(self):
        return RobotWorldIterator(self._all_robots)
        
    
    def build_robot(self, robot_name=None, rx=None, ry=None, scale=1):
        
        r = Robot(name=robot_name, x=rx, y=ry, scale=scale)
        
        if robot_name== None:
            r.set_name("noname " + str(self._robot_counter))
        
        self._robot_counter += 1
        self._robot_by_name[r.get_name()] = r
        self._all_robots.append(r)
        
        return r 
    
    
    def get_robots_count(self):
        return self._robot_counter
    

class RobotWorldIterator:
    def __init__(self, robots):
        self._all_robots = robots
        self._i = 0
    
    
    def __iter__(self):
        return self
    
    
    def __next__(self):
        if self._i<len(self._all_robots):
            result = self._all_robots[self._i]
            self._i += 1
            return result 
        else:
            raise StopIteration()
        
    
        
    