'''RemoteClient class
'''
import uuid
import json
from deepspace.singleton import Singleton
from deepspace.math2d import Point2d
import deepspace.messages
from tornado.websocket import WebSocketHandler
from tornado import gen


class RemoteClientRegistry(Singleton):
    'singleton Storage for remote clients'
    _remote_clients = {}

    def __init__(self):
        super(RemoteClientRegistry, self).__init__()

    def add_remote_client(self, remote_client):
        'add remote client int singleton storage'
        self._remote_clients[remote_client.uuid] = remote_client

    def del_remote_client(self, remote_client):
        'del remote client'
        if self._remote_clients.__contains__(remote_client.uuid):
            del self._remote_clients[remote_client.uuid]

    def get_client_count(self):
        'returns client count'
        return len(self._remote_clients)

    def items(self):
        'return keys, values for iteration'
        return self._remote_clients.items()


class VisibleCharacter(object):
    'data structure for visible character'
    def __init__(self, character, command):
        self.character = character
        self.command = command


class RemoteClient(WebSocketHandler):
    '''WebSocket message handler
    handles client io
    '''
    def __init__(self, application, request):
        super(RemoteClient, self).__init__(application, request)

        self.visible_characters = {}
        self.world_position = Point2d()
        self.display_width = 1920
        self.display_height = 1080
        self.uuid = ""
        self.uuid = uuid.uuid4().hex


    def open(self):
        registry = RemoteClientRegistry()
        registry.add_remote_client(self)
        print("WebSocket opened:", self.uuid)


    def on_message(self, message):
        print("ON_MESSAGE:",self.uuid)
        self.parse_client_message(message)


    def on_close(self):
        registry = RemoteClientRegistry()
        registry.del_remote_client(self)
        self.visible_characters.clear()
        print("WebSocket closed:", self.uuid)


    def check_origin(self, origin):
        return True


    def parse_client_message(self, message):
        'parse message and dispatch it'
        try:
            message_object = json.loads(message)
            print(message)

            if deepspace.messages.is_valid_mouse_command(message_object):
                self.on_client_mouse_event(message_object)
            else:
                print("Invalid message")

        except BaseException as err:
            print("Exception:", err)
            print("Wrong message",message)


    def on_client_mouse_event(self, message_object):
        'process mouse event'
        pass


    def is_point_visible(self, world_position):
        'checks is point visible in camera'
        point_a = Point2d()
        point_b = Point2d()

        point_a.x = self.world_position.x - self.display_width / 2
        point_a.y = self.world_position.y - self.display_width / 2

        point_b.x = self.world_position.x + self.display_height / 2
        point_b.y = self.world_position.y + self.display_width  / 2

        if (point_a.x <= world_position.x and world_position.x <= point_b.x) and (point_a.y <= world_position.y and world_position.y <= point_b.y):
            return True
        return False


    def update_visible_character(self, character):
        'append visible character'
        if self.is_point_visible(character.world_position):
            if self.visible_characters.__contains__(character.uuid):
                self.visible_characters[character.uuid].command = "update"
            else:
                self.visible_characters[character.uuid] = VisibleCharacter(character,"add")
        else:
            if self.visible_characters.__contains__(character.uuid):
                if self.visible_characters[character.uuid].command == "delete":
                    del self.visible_characters[character.uuid]
                else:
                    self.visible_characters[character.uuid].command = "delete"


    @gen.coroutine
    def update_remote_client(self):
        'send data to remote clinet'
        entities = []
        
        for _, visible_character in self.visible_characters.items():

            
            if visible_character.character.client_should_be_refreshed is True or visible_character.command in ("add","delete"):
                
                entities.append({"name":visible_character.character.uuid,
                                 "x":visible_character.character.world_position.x,
                                 "y":visible_character.character.world_position.y,
                                 "scale":visible_character.character.scale,
                                 "command":visible_character.command,
                                 "speed_x":visible_character.character.speed_x,
                                 "speed_y":visible_character.character.speed_y})

        result = json.dumps(entities)
        yield self.write_message(result)


