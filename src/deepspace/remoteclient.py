'''RemoteClient class
'''
import uuid
from deepspace.singleton import Singleton
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


class RemoteClient(WebSocketHandler):
    '''WebSocket message handler
    handles client io
    '''
    def __init__(self, application, request):
        WebSocketHandler.__init__(self, application, request)
        self._id = uuid.uuid4()

    def open(self):
        registry = RemoteClientRegistry()
        registry.add_remote_client(self)
        print("WebSocket opened:", self._id)

    def on_message(self, message):
        pass

    def on_close(self):
        registry = RemoteClientRegistry()
        registry.del_remote_client(self)
        print("WebSocket closed:", self._id)

    def check_origin(self, origin):
        return True

    def get_uuid(self):
        'returns unique client id'
        return self._id
