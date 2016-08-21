'''Main function
'''
import json
import time

import tornado.ioloop
import tornado.web


from tornado import gen
from deepspace.world import World
from deepspace.remoteclient import RemoteClient
from deepspace.behaviour import LinearMovement
from deepspace.math2d import Point2d

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
    #world.build_character(name="Alex",position_x=50,position_y=50,scale = 0.5)
    #world.build_character("Boris", position_x=150, position_y=150, scale = 0.2)

    moving_character = world.build_character("Anatoliy", position_x=250, position_y=250, scale=0.2)

    point_from  = Point2d()
    point_from.set_xy(0, 0)

    point_to    = Point2d()
    point_to.set_xy(200, 200)

    linear_movement = LinearMovement(point_from, point_to, 10)
    moving_character.add_behaviour(linear_movement)


@gen.coroutine
def updater():
    'update world coroutine'
    start_time = time.time()
    while True:
        yield gen.sleep(0.1)
        elapsed_time = time.time() - start_time
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
