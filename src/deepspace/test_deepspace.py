"""Unit tests for deepspace
"""
import unittest
import uuid
import json
import sys

from deepspace.world import World
from mock.mock import MagicMock


class TestBaseCharacterFunctions(unittest.TestCase):
    """Unit tests for basic characters and world functions
    """

    def test_basic_behaviour(self):
        """Test for basic behaviour
        """
        from deepspace.behaviour import AbstractAnimator

        class SimpleIncrementXOnce(AbstractAnimator):
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
        registry1.del_all_remote_clients()

        class RemoteClientStub(object):
            'stub for RemoteClient'
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


    def test_remote_client_linear_movement(self):
        '''Test for linear movement
        1) create remote client object
        2) add mouse event
        3) simulate
        4) check results and mocks
        '''
        from deepspace.remoteclient import RemoteSocketHandler
        from deepspace.remoteclient import RemoteClient

        class mockRemoteSocketHandler(RemoteSocketHandler):
            'fake socket handler'
            def __init__(self):
                '__init__ is not called intentionally'
                self.remote_client = RemoteClient()
        
        verbose_mode = False
        
        def debug_print(*params, sep=' ', end='\n', file=sys.stdout, flush=False):
            if verbose_mode:
                print(*params)
        
        def print_world_position(text, visible_object):
            if not verbose_mode: 
                return
            
            print(text, "x=",visible_object.world_position.x,"y=", visible_object.world_position.y)

        def simulate_world(elapsed_time):
            world.update_world(elapsed_time)
            #####################
            # simulate world.update_clients() without yield
            for _, client in world.remote_clients.items():
                message = client.get_message_for_remote_client()
                #yield client.socket.write_message(message)
            for character in world:
                character.client_should_be_refreshed = False
            #####################
            
        world = World()
        world.delete_all_objects()
        
        remote_socket_handler_1 = mockRemoteSocketHandler()
        remote_socket_handler_1.open()
        
        remote_socket_handler_2 = mockRemoteSocketHandler()
        remote_socket_handler_2.open()

        self.assertIsNotNone(remote_socket_handler_1.remote_client, "RemoteClient1 is not initiated")
        self.assertIsNotNone(remote_socket_handler_2.remote_client, "RemoteClient2 is not initiated")
        
        remote_client_1 = remote_socket_handler_1.remote_client
        remote_client_2 = remote_socket_handler_2.remote_client
        
        remote_client_1.uuid = "client_1"
        remote_client_2.uuid = "client_2"

        self.assertIsNotNone(world._character_by_uuid[remote_client_1.client_visible_character.uuid],"RemoteClientvisibleobject1 is not initiated")
        self.assertIsNotNone(world._character_by_uuid[remote_client_2.client_visible_character.uuid],"RemoteClientvisibleobject2 is not initiated")

        client_visible_object_1 = remote_client_1.client_visible_character
        client_visible_object_2 = remote_client_2.client_visible_character
        
        client_visible_object_1.uuid = "object_1"
        client_visible_object_2.uuid = "object_2"
        
        client_visible_object_1.world_position.x = 0
        client_visible_object_1.world_position.y = 0
        client_visible_object_1.client_should_be_refreshed = True
        remote_client_1.world_position.x = client_visible_object_1.world_position.x
        remote_client_1.world_position.y = client_visible_object_1.world_position.y

        client_visible_object_2.world_position.x = 300
        client_visible_object_2.world_position.y = 0
        client_visible_object_2.client_should_be_refreshed = True
        remote_client_2.world_position.x = client_visible_object_2.world_position.x
        remote_client_2.world_position.y = client_visible_object_2.world_position.y
        
        debug_print("Simulation 0")
        simulate_world(1)
                
        print_world_position("O1.0) world",client_visible_object_1)
        print_world_position("O2.0) world",client_visible_object_2)
        
        self.assertEqual(remote_client_1.world_position.x, 0, "RemoteClient.x is not on 0 point")
        self.assertEqual(remote_client_1.world_position.y, 0, "RemoteClient.y is not on 0 point")

        self.assertEqual(remote_client_2.world_position.x, 300, "RemoteClient.x is not on world 1000")
        self.assertEqual(remote_client_2.world_position.y, 0, "RemoteClient.y is not on world 0")
        
        mouse_message_1 = {}
        mouse_message_1["command"] = "mouse_click"
        mouse_message_1["button"] = 1
        mouse_message_1["x"] = 300 # client coordinates
        mouse_message_1["y"] = 0
        
        client_visible_object_1.max_speed = 50
        remote_client_1.on_client_mouse_event(mouse_message_1)
        
        debug_print("Simulation 1")
        debug_print("client_1:",mouse_message_1)
        simulate_world(1)
                
        print_world_position("O1.1) world",client_visible_object_1)
        print_world_position("O2.1) world",client_visible_object_2)
        
        self.assertEqual(remote_client_1.world_position.x, 50, "RemoteClient.x is not on 50 point")
        self.assertEqual(remote_client_1.world_position.y, 0, "RemoteClient.y is not on 0 point")

        self.assertEqual(remote_client_2.world_position.x, 300, "RemoteClient.x is not on world 300")
        self.assertEqual(remote_client_2.world_position.y, 0, "RemoteClient.y is not on world 0")        

        debug_print("Simulation 2")        
        simulate_world(1)
        
        print_world_position("O1.2) world",client_visible_object_1)
        print_world_position("O2.2) world",client_visible_object_2)

        self.assertEqual(remote_client_1.world_position.x, 100, "RemoteClient.x is not on 100 point")
        self.assertEqual(remote_client_1.world_position.y, 0, "RemoteClient.y is not on 0 point")

        self.assertEqual(remote_client_2.world_position.x, 300, "RemoteClient.x is not on world 300")
        self.assertEqual(remote_client_2.world_position.y, 0, "RemoteClient.y is not on world 0")      
        
        mouse_message_2 = {}
        mouse_message_2["command"] = "mouse_click"
        mouse_message_2["button"] = 1
        mouse_message_2["x"] = -300 # client coordinates
        mouse_message_2["y"] = 0
        
        client_visible_object_2.max_speed = 50
        remote_client_2.on_client_mouse_event(mouse_message_2)

        debug_print("Simulation 3")        
        debug_print("client_2:",mouse_message_2)
        simulate_world(1)
        
        print_world_position("O1.3) world",client_visible_object_1)
        print_world_position("O2.3) world",client_visible_object_2)
        
        self.assertEqual(remote_client_1.world_position.x, 150, "RemoteClient.x is not on 150 point")
        self.assertEqual(remote_client_1.world_position.y, 0, "RemoteClient.y is not on 0 point")

        self.assertEqual(remote_client_2.world_position.x, 250, "RemoteClient.x is not on world 250")
        self.assertEqual(remote_client_2.world_position.y, 0, "RemoteClient.y is not on world 0")           

        debug_print("Simulation 4")        
        simulate_world(1)
        
        print_world_position("O1.4) world",client_visible_object_1)
        print_world_position("O2.4) world",client_visible_object_2)
        
        self.assertEqual(remote_client_1.world_position.x, 200, "RemoteClient.x is not on 200 point")
        self.assertEqual(remote_client_1.world_position.y, 0, "RemoteClient.y is not on 0 point")

        self.assertEqual(remote_client_2.world_position.x, 200, "RemoteClient.x is not on world 200")
        self.assertEqual(remote_client_2.world_position.y, 0, "RemoteClient.y is not on world 0")          

        debug_print("Simulation 5")        
        simulate_world(1)
        
        print_world_position("O1.5) world",client_visible_object_1)
        print_world_position("O2.5) world",client_visible_object_2)

        debug_print("Simulation 6")        
        simulate_world(1)
        
        print_world_position("O1.6) world",client_visible_object_1)
        print_world_position("O2.6) world",client_visible_object_2)

        debug_print("Simulation 7")        
        simulate_world(1)
        
        print_world_position("O1.7) world",client_visible_object_1)
        print_world_position("O2.7) world",client_visible_object_2)

        debug_print("Simulation 8")        
        simulate_world(1)
        
        print_world_position("O1.8) world",client_visible_object_1)
        print_world_position("O2.8) world",client_visible_object_2)

        debug_print("Simulation 9")        
        simulate_world(1)
        
        print_world_position("O1.9) world",client_visible_object_1)
        print_world_position("O2.9) world",client_visible_object_2)
        
        self.assertEqual(remote_client_1.world_position.x, 300, "RemoteClient.x is not on 300 point")
        self.assertEqual(remote_client_1.world_position.y, 0, "RemoteClient.y is not on 0 point")

        self.assertEqual(remote_client_2.world_position.x, 0, "RemoteClient.x is not on world 0")
        self.assertEqual(remote_client_2.world_position.y, 0, "RemoteClient.y is not on world 0")         
