'''Main function
'''
import json
import time

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
    from deepspace.worldbuilder import WorldBuilder
    from deepspace.worldbuilder import TestWorldGenerator

    world_builder = WorldBuilder()
    world_builder.build_world(world, TestWorldGenerator())
    

@gen.coroutine
def updater():
    'update world coroutine'
    start_time = time.time()
    while True:
        yield gen.sleep(0.1)
        elapsed_time = time.time() - start_time
        start_time = time.time()
        world.update_world(elapsed_time)


@gen.coroutine
def updater_clients():
    'update remote clients'
    while True:
        yield gen.sleep(0.1)
        world.update_clients()

world = World()

if __name__ == "__main__":
    init_world()
    tornado.ioloop.IOLoop.current().add_callback(updater)
    tornado.ioloop.IOLoop.current().add_callback(updater_clients)
    application_instance = make_app()
    application_instance.listen(8888)
    tornado.ioloop.IOLoop.current().start()
