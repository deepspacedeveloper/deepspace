"""Deep Space World
"""
from tornado import gen
from deepspace.character import Character
from deepspace.remoteclient import RemoteClientRegistry
from deepspace.singleton import Singleton

class World(Singleton):
    """World contains all characters
    """

    def __init__(self):
        self._character_counter = 0
        self._character_by_name = {}
        self._all_characters = []
        self.remote_clients = RemoteClientRegistry()

    def __iter__(self):
        return WorldIterator(self._all_characters)


    def build_character(self, name=None, position_x=None, position_y=None, scale=1):
        """Build character and attach to world
        """

        new_character = Character(name = name, x = position_x, y = position_y, scale = scale)

        if name is None:
            new_character.set_name("noname " + str(self._character_counter))

        self._character_counter += 1
        self._character_by_name[new_character.get_name()] = new_character
        self._all_characters.append(new_character)

        return new_character


    def get_characters_count(self):
        """Return count of attached characters
        """
        return self._character_counter


    def update_world(self, elapsed_time):
        ' update all world'

        for character in self:
            character.update(elapsed_time)

            for _, client in self.remote_clients.items():
                client.update_visible_character(character)


    @gen.coroutine
    def update_clients(self):
        'update remote clients'
        for _, client in self.remote_clients.items():
            client.update_remote_client()
        
        for character in self:
            character.client_should_be_refreshed = False


class WorldIterator:
    """Iterator for CharacterWorld
    """
    def __init__(self, robots):
        self._all_characters = robots
        self._iterator_position = 0


    def __iter__(self):
        return self


    def __next__(self):
        if self._iterator_position<len(self._all_characters):
            result = self._all_characters[self._iterator_position]
            self._iterator_position += 1
            return result
        else:
            raise StopIteration()


