"""Deepspace World
"""
from deepspace.character import Character


class World:
    """World contains all characters
    """

    def __init__(self):
        self._robot_counter = 0
        self._robot_by_name = {}
        self._all_robots = []


    def __iter__(self):
        return WorldIterator(self._all_robots)


    def build_character(self, name=None, position_x=None, position_y=None, scale=1):
        """Build character and attach to world
        """

        new_robot = Character(name = name, x = position_x, y = position_y, scale = scale)

        if name == None:
            new_robot.set_name("noname " + str(self._robot_counter))

        self._robot_counter += 1
        self._robot_by_name[new_robot.get_name()] = new_robot
        self._all_robots.append(new_robot)

        return new_robot


    def get_characters_count(self):
        """Return count of attached characters
        """
        return self._robot_counter


class WorldIterator:
    """Iterator for CharacterWorld
    """
    def __init__(self, robots):
        self._all_robots = robots
        self._iterator_position = 0


    def __iter__(self):
        return self


    def __next__(self):
        if self._iterator_position<len(self._all_robots):
            result = self._all_robots[self._iterator_position]
            self._iterator_position += 1
            return result
        else:
            raise StopIteration()


