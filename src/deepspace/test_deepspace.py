"""Unit tests for deepspace
"""
import unittest

from wor.character import Character
from wor.world import World


class TestBaseCharacterFunctions(unittest.TestCase):
    """Unit tests for basic characters and world functions
    """

    def test_initRobot(self):
        
        robot = Character()
        
        self.assertEqual(robot.get_name(), "noname", "Bad robot's name. It should be 'noname'")
        
        r = Character(name="Vasya")
        self.assertEqual(r.get_name(), "Vasya", "Bad robot's name. It should be 'Vasya'")
        
        
    def test_world_createrobot(self):

        w = World()
        
        r0 = w.build_character()

        self.assertEqual(r0.get_name(), "noname 0", "Bad robot name. It must be 'noname 0'")
        self.assertEqual(w.get_characters_count(), 1, "Bad robots count. It must be 1")

        r1 = w.build_character()
        
        self.assertEqual(r1.get_name(), "noname 1", "Bad robot name. It must be 'noname 1'")
        self.assertEqual(w.get_characters_count(), 2, "Bad robots count. It must be 2")


    def test_worldIterator(self):

        w = World()
        for i in "12345":
            w.build_character(i)
        
        self.assertEqual(w.get_characters_count(), 5, "Wrong robot count")
        
        i = 1
        for robot in w:
                self.assertEqual(robot.get_name(), str(i), "Wrong robot name")
                i += 1
        
        
        
