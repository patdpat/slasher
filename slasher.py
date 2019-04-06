import arcade
from models import World
 
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400


class ModelSprite(arcade.Sprite):

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
 
    def draw(self):
        self.sync_with_model()
        super().draw()
 
 
class DotRunWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)  
        arcade.set_background_color(arcade.color.GRAY)

        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.dot_sprite = ModelSprite('images/dot.png', model=self.world.dot)

    def update(self, delta):
        self.world.update(delta)
 
    def on_draw(self):
        arcade.start_render()
        self.dot_sprite.draw()

if __name__ == '__main__':
    window = DotRunWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
