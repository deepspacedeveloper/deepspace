'''Math for 2d space
'''

class Point2d(object):
    'Point in 2d space'
    def __init__(self):
        super(Point2d, self).__init__()
        self.x = 0
        self.y = 0

    def set_xy(self, x, y):
        self.x = x
        self.y = y 

class Rectangle(object):
    'Rectangle'
    point_a = Point2d()
    point_b = Point2d()
