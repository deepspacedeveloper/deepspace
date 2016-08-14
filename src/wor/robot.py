class Robot():
    def __init__(self, name=None, x=0, y=0, scale=1):
        self._x = x
        self._y = y
        self.scale = scale
        if name == None:
            self._name = "noname"
        else:
            self._name = name
        
    def get_name(self):
        return self._name

    
    def set_name(self, name):
        self._name = name
        
        
    def get_x(self):
        return self._x
    
    
    def get_y(self):
        return self._y
    
    def update(self):
        self._x += 1
