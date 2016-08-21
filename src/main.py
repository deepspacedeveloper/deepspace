'''Main function
'''
import json

import tornado.ioloop
import tornado.web


from tornado import gen
from deepspace.world import World
from deepspace.remoteclient import RemoteClient

class MainHandler(tornado.web.RequestHandler):
    'simple method get. It should be refactored into trash'
    def get(self):
        self.write("Hello, world")


class EntityHandler(tornado.web.RequestHandler):
    'TODO refactor me'
    def get(self):
        global world

        entities = []

        for robot in world:
            entities.append({"name":robot.get_name(), "x":robot.get_x(), "y":robot.get_y()})

        result = json.dumps(entities)

        self.write(result)


def make_app():
    'init tornado web app'
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/entity", EntityHandler),
        (r"/websocket", RemoteClient)
    ])


def init_world():
    'init world. it should be refactored'
    global world
    world.build_character(name="Alex",position_x=50,position_y=50,scale = 0.5)
    world.build_character("Boris", position_x=150, position_y=150, scale = 0.2)
    world.build_character("Anatoliy", position_x=250, position_y=250)


@gen.coroutine
def updater():
    'update world coroutine'
    while True:
        yield gen.sleep(0.1)
        world.update_world()



@gen.coroutine
def updater_clients():
    'update remote clients'
    print("Starting updating clients...")
    while True:
        print("Updating clients...")
        yield gen.sleep(1)
        world.update_clients()

world = World()

if __name__ == "__main__":
    init_world()
    tornado.ioloop.IOLoop.current().add_callback(updater)
    tornado.ioloop.IOLoop.current().add_callback(updater_clients)
    application_instance = make_app()
    application_instance.listen(8888)
    tornado.ioloop.IOLoop.current().start()
