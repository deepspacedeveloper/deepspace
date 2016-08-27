"""Unit tests for deepspace
"""
import unittest
import uuid
import json

from deepspace.world import World


class TestBaseCharacterFunctions(unittest.TestCase):
    """Unit tests for basic characters and world functions
    """

    def test_basic_behaviour(self):
        """Test for basic behaviour
        """
        from deepspace.behaviour import BaseBehaviour

        class SimpleIncrementXOnce(BaseBehaviour):
            """increate position_x once
            """
            counter = 0

            def animate(self, elapsed_time):
                self.character.world_position.x += 10
                self.counter += 1

            def is_done(self):
                if self.counter >= 1:
                    return True
                return False


        world = World()
        character = world.build_character(0, 0, 1)
        behaviour = SimpleIncrementXOnce()
        character.add_behaviour(behaviour)

        character.update(1)

        self.assertEqual(character.world_position.x, 10, "Behaivour doesnot work")

        character.update(1)

        self.assertEqual(character.world_position.x, 10, "Behaivour doesnot deleted")


    def test_singleton(self):
        'test singleton pattern'
        from deepspace.singleton import Singleton

        class StringSingleton(Singleton):
            'test singleton class'
            def __init__(self, str_val):
                super(StringSingleton, self).__init__()
                self.str_val = str_val

        singleton1 = StringSingleton("test1")
        singleton2 = StringSingleton("test2")

        singleton1.str_val = "super string"

        self.assertEqual(singleton1.str_val, singleton2.str_val, "Singletons must be equal")


    def test_remote_client_registry(self):
        'test for singleton registry'
        from deepspace.remoteclient import RemoteClientRegistry

        registry1 = RemoteClientRegistry()
        registry2 = RemoteClientRegistry()

        class RemoteClientStub(object):
            'stub for RemoteClient'
            self.uuid = ""
            def __init__(self):
                self.uuid = uuid.uuid4().hex


        client1 = RemoteClientStub()
        client2 = RemoteClientStub()

        registry1.add_remote_client(client1)
        registry2.add_remote_client(client2)

        self.assertEqual(registry1.get_client_count(), 2, "Registry must contain 2 elements")
        self.assertEqual(registry1, registry2, "Registeries should be the same instance")


    def test_visible_character(self):
        'test for data structure'
        from deepspace.remoteclient import VisibleCharacter

        visible_character = VisibleCharacter(1,"add")

        self.assertEqual(visible_character.command, "add",
                         "Visible character is broken")

        self.assertEqual(visible_character.character, 1,
                         "Visible character is broken 1")


    def test_websocket_mouse_validator(self):
        'test mouse click command validator'
        from deepspace.messages import is_valid_mouse_command

        mouse_command = {}

        message_string = json.dumps(mouse_command)
        message_object = json.loads(message_string)
        self.assertNotEqual(is_valid_mouse_command(message_object), True,
                            "Validator is broken. It is wrong message 1")

        mouse_command["command"]="mouse_cl"

        message_string = json.dumps(mouse_command)
        message_object = json.loads(message_string)
        self.assertNotEqual(is_valid_mouse_command(message_object), True,
                            "Validator is broken. It is wrong message 2")

        mouse_command["command"]="mouse_click"
        mouse_command["button"]=1
        mouse_command["x"]=50
        mouse_command["y"]=20

        message_string = json.dumps(mouse_command)
        message_object = json.loads(message_string)
        self.assertEqual(is_valid_mouse_command(message_object), True,
                         "Validator is broken. It is valid message")

