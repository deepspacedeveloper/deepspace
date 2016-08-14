"""Unit tests for deepspace
"""
import unittest

from deepspace.character import Character
from deepspace.world import World


class TestBaseCharacterFunctions(unittest.TestCase):
    """Unit tests for basic characters and world functions
    """

    def test_base_initialisation(self):
        """Test basic initialisation
        """
        robot = Character()

        self.assertEqual(robot.get_name(), "noname", "Bad robot's name. It should be 'noname'")

        character = Character(name="Vasya")
        self.assertEqual(character.get_name(), "Vasya", "Bad robot's name. It should be 'Vasya'")


    def test_build_character(self):
        """Test for basic world functions
        """

        world = World()

        character_1 = world.build_character()

        self.assertEqual(character_1.get_name(),
                         "noname 0", "Bad robot name. It must be 'noname 0'")
        self.assertEqual(world.get_characters_count(), 1,
                         "Bad robots count. It must be 1")

        character_2 = world.build_character()

        self.assertEqual(character_2.get_name(),
                         "noname 1", "Bad robot name. It must be 'noname 1'")
        self.assertEqual(world.get_characters_count(), 2,
                         "Bad robots count. It must be 2")


    def test_world_iterator(self):
        """Test for world iterator
        """

        world = World()
        for i in "12345":
            world.build_character(i)

        self.assertEqual(world.get_characters_count(), 5, "Wrong robot count")

        i = 1
        for robot in world:
            self.assertEqual(robot.get_name(), str(i), "Wrong robot name")
            i += 1

    def test_basic_behaviour(self):
        """Test for basic behaviour
        """
        from deepspace.behaviour import BaseBehaviour

        class SimpleIncrementXOnce(BaseBehaviour):
            """increate position_x once
            """
            counter = 0

            def animate(self):
                self._character.set_x(self._character.get_x()+10)
                self.counter += 1

            def is_done(self):
                if self.counter >= 1:
                    return True
                return False


        world = World()
        character = world.build_character("test", 0, 0, 1)
        behaviour = SimpleIncrementXOnce()
        character.add_behaviour(behaviour)

        character.update()

        self.assertEqual(character.get_x(), 10, "Behaivour doesnot work")

        character.update()

        self.assertEqual(character.get_x(), 10, "Behaivour doesnot deleted")
