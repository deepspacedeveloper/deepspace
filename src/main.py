import tornado.ioloop
import tornado.web
import json
import uuid


from tornado.websocket import WebSocketHandler

from wor.world import RobotWorld
from tornado import gen

websockets = {}

class EchoWebSocket(WebSocketHandler):
    def __init__(self, application, request):
        WebSocketHandler.__init__(self, application, request)
        self._id = uuid.uuid4()
    
    def open(self):
        global websockets
        websockets[self._id] = self
        print("WebSocket opened:", self._id)

    def on_message(self, message):
        pass

    def on_close(self):
        print("WebSocket closed:", self._id)
    
    def check_origin(self, origin):
        return True        


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class EntityHandler(tornado.web.RequestHandler):
    def get(self):
        global world

        entities = []
        
        for robot in world:
            entities.append({"name":robot.get_name(), "x":robot.get_x(), "y":robot.get_y()}) 
        
        result = json.dumps(entities)
                
        self.write(result)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/entity", EntityHandler),
        (r"/websocket", EchoWebSocket)
    ])


def init_world():
        global world
        
        world.build_robot("Alex", rx=50, ry=50, scale = 0.5)
        world.build_robot("Boris", rx=150, ry=150, scale = 0.2)
        world.build_robot("Anatoliy", rx=250, ry=250)


@gen.coroutine
def updater():
    global world
    while True:
        yield gen.sleep(0.1)
        
        for robot in world:
            robot.update()

@gen.coroutine
def updater_clients():
    global world
    global websockets
    
    while True:
        yield gen.sleep(0.1)
        
        for key, client in websockets.items():
            
            entities = []
            
            for robot in world:
                entities.append({"name":robot.get_name(), "x":robot.get_x(), "y":robot.get_y(), "scale":robot.scale}) 
            
            result = json.dumps(entities)
            
            print("writing for:", key)
            client.write_message(result)

    
    
world = RobotWorld()

if __name__ == "__main__":
    init_world()
    tornado.ioloop.IOLoop.current().add_callback(updater)
    tornado.ioloop.IOLoop.current().add_callback(updater_clients)
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
