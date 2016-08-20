'''RemoteClient class
'''
import uuid
import json
from deepspace.singleton import Singleton
from deepspace.math2d import Point2d
import deepspace.messages
from tornado.websocket import WebSocketHandler


class RemoteClientRegistry(Singleton):
    'singleton Storage for remote clients'
    def __init__(self):
        super(RemoteClientRegistry, self).__init__()
        self._remote_clients = {}

    def add_remote_client(self, remote_client):
        'add remote client int singleton storage'
        self._remote_clients[remote_client.get_uuid()] = remote_client

    def del_remote_client(self, remote_client):
        'del remote client'
        del self._remote_clients[remote_client.get_uuid()]

    def get_client_count(self):
        'returns client count'
        return len(self._remote_clients)

    def items(self):
        'return keys, values for iteration'
        return self._remote_clients.items()


class VisibleCharacter(object):
    'data structure for visible character'
    __slots__ = ("character", "need_to_be_refreshed")


class RemoteClient(WebSocketHandler):
    '''WebSocket message handler
    handles client io
    '''
    visible_characters = {}
    camera_position = Point2d()
    display_width = 640
    display_height = 480


    def __init__(self, application, request):
        WebSocketHandler.__init__(self, application, request)
        self._id = uuid.uuid4()


    def open(self):
        registry = RemoteClientRegistry()
        registry.add_remote_client(self)
        print("WebSocket opened:", self._id)


    def on_message(self, message):
        print("ON_MESSAGE:",self.get_uuid())
        self.parse_client_message(message)


    def on_close(self):
        registry = RemoteClientRegistry()
        registry.del_remote_client(self)
        print("WebSocket closed:", self._id)


    def check_origin(self, origin):
        return True


    def get_uuid(self):
        'returns unique client id'
        return self._id


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
