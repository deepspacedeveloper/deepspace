import unittest

from wor.robot import Robot
from wor.world import RobotWorld

class TestRobot(unittest.TestCase):
    
    def test_initRobot(self):
        
        robot = Robot()
        
        self.assertEqual(robot.get_name(), "noname", "Bad robot's name. It should be 'noname'")
        
        r = Robot(name="Vasya")
        self.assertEqual(r.get_name(), "Vasya", "Bad robot's name. It should be 'Vasya'")
        
        
    def test_world_createrobot(self):

        w = RobotWorld()
        
        r0 = w.build_robot()

        self.assertEqual(r0.get_name(), "noname 0", "Bad robot name. It must be 'noname 0'")
        self.assertEqual(w.get_robots_count(), 1, "Bad robots count. It must be 1")

        r1 = w.build_robot()
        
        self.assertEqual(r1.get_name(), "noname 1", "Bad robot name. It must be 'noname 1'")
        self.assertEqual(w.get_robots_count(), 2, "Bad robots count. It must be 2")


    def test_worldIterator(self):

        w = RobotWorld()
        for i in "12345":
            w.build_robot(i)
        
        self.assertEqual(w.get_robots_count(), 5, "Wrong robot count")
        
        i = 1
        for robot in w:
                self.assertEqual(robot.get_name(), str(i), "Wrong robot name")
                i += 1
        
        
        
