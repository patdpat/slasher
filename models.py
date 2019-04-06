GRAVITY = -1
MAX_VX = 10
ACCX = 1
 
class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0
 
 
class Dot(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)
        self.vx = 0
        self.vy = 0
 
    def update(self, delta):
        if self.vx < MAX_VX:
            self.vx += ACCX
 
        self.x += self.vx
 
 
class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
 
        self.dot = Dot(self, 0, 100)
 
 
    def update(self, delta):
        self.dot.update(delta)