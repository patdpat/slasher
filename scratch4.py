import arcade
import os
import random
import math
import time
from go import *

SPRITE_SCALING = 0.1
SPRITE_SCALING_FROG = 0.3

FROG_COUNT = 28
BOUNCING_FROG_COUNT = 8
CIRCLR_FROG_COUNT = 4
FROG_SPEED = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "SUCK MY DICK"

MOVEMENT_SPEED = 5
SPRITE_SPEED = 0.5


def make_star_field(star_count):

    shape_list = arcade.ShapeElementList()

    for star_no in range(star_count):
        x = random.randrange(SCREEN_WIDTH)
        y = random.randrange(SCREEN_HEIGHT)
        radius = random.randrange(1, 4)
        brightness = random.randrange(127, 256)
        color = (brightness, brightness, brightness)
        shape = arcade.create_ellipse_filled(
            x, y, radius, radius, color, num_segments=8)
        shape_list.append(shape)

    return shape_list


def make_skyline(width, skyline_height, skyline_color,
                 gap_chance=0.70, window_chance=0.30, light_on_chance=0.5,
                 window_color=(255, 255, 200), window_margin=3, window_gap=2,
                 cap_chance=0.20):

    shape_list = arcade.ShapeElementList()

    shape = arcade.create_rectangle_filled(
        width / 2, skyline_height / 2, width, skyline_height, skyline_color)
    shape_list.append(shape)

    building_center_x = 0
    while building_center_x < width:

        if random.random() < gap_chance:
            gap_width = random.randrange(10, 50)
        else:
            gap_width = 0

        # Figure out location and size of building
        building_width = random.randrange(20, 70)
        building_height = random.randrange(40, 150)
        building_center_x += gap_width + (building_width / 2)
        building_center_y = skyline_height + (building_height / 2)

        # Add building to the list
        shape = arcade.create_rectangle_filled(building_center_x, building_center_y,
                                               building_width, building_height, skyline_color)
        shape_list.append(shape)

        if random.random() < cap_chance:
            x1 = building_center_x - building_width / 2
            x2 = building_center_x + building_width / 2
            x3 = building_center_x

            y1 = y2 = building_center_y + building_height / 2
            y3 = y1 + building_width / 2

            shape = arcade.create_polygon(
                [[x1, y1], [x2, y2], [x3, y3]], skyline_color)
            shape_list.append(shape)

        if random.random() < window_chance:

            window_rows = random.randrange(10, 15)
            window_columns = random.randrange(1, 7)

            window_height = (building_height - window_margin * 2) / window_rows
            window_width = (building_width - window_margin * 2 -
                            window_gap * (window_columns - 1)) / window_columns

            building_base_y = building_center_y - building_height / 2
            building_left_x = building_center_x - building_width / 2

            for row in range(window_rows):
                for column in range(window_columns):
                    if random.random() < light_on_chance:
                        window_y = building_base_y + row * window_height + window_height / 2
                        window_x = building_left_x + column * \
                            (window_width + window_gap) + \
                            window_width / 2 + window_margin
                        shape = arcade.create_rectangle_filled(window_x, window_y,
                                                               window_width, window_height * 0.8, window_color)
                        shape_list.append(shape)

        building_center_x += (building_width / 2)

    return shape_list


class Timer():
    def __init__(self):
        from time import perf_counter as time
        self.time = time
        self.start_time = self.time()

    def current_time(self):
        return self.time() - self.start_time

    def reset(self):
        self.start_time = self.time()

    def set_time_limit(self, new_time):
        self.time_limit = new_time

    def get_remaining_time(self):
        self.time_limit - self.current_time()


class Player(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)
        self.stars = make_star_field(150)
        self.skyline1 = make_skyline(SCREEN_WIDTH * 5, 250, (80, 80, 80))
        self.skyline2 = make_skyline(SCREEN_WIDTH * 5, 150, (50, 50, 50))

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.frog_list = None
        # Set up the player info
        self.player_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.frog_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        self.player_sprite = Player("images/character.png", SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        for i in range(FROG_COUNT):
            frog_face = random.randint(1, 8)
            if frog_face == 1:
                frog = Frog("images/frog/frog1.png", SPRITE_SCALING_FROG)
            if frog_face == 2:
                frog = Frog("images/frog/frog2.png", SPRITE_SCALING_FROG)
            if frog_face == 3:
                frog = Frog("images/frog/frog3.png", SPRITE_SCALING_FROG)
            if frog_face == 4:
                frog = Frog("images/frog/frog4.png", SPRITE_SCALING_FROG)
            if frog_face == 5:
                frog = Frog("images/frog/frog5.png", SPRITE_SCALING_FROG)
            if frog_face == 6:
                frog = Frog("images/frog/frog6.png", SPRITE_SCALING_FROG)
            if frog_face == 7:
                frog = Frog("images/frog/frog7.png", SPRITE_SCALING_FROG)
            frog.center_x = random.randrange(SCREEN_WIDTH)
            frog.center_y = random.randrange(SCREEN_HEIGHT)
            self.frog_list.append(frog)

        for i in range(BOUNCING_FROG_COUNT):
            bouncing_frog = BouncingFrog(
                "images/frog/frog8.png", SPRITE_SCALING_FROG)
            bouncing_frog.center_x = random.randrange(SCREEN_WIDTH)
            bouncing_frog.center_y = random.randrange(SCREEN_HEIGHT)
            bouncing_frog.change_x = random.randrange(-3, 4)
            bouncing_frog.change_y = random.randrange(-3, 4)
            self.frog_list.append(bouncing_frog)
        for i in range(CIRCLR_FROG_COUNT):
            circle_frog = CircleFrog(
                "images/frog/frog9.png", SPRITE_SCALING_FROG)
            circle_frog.circle_center_x = random.randrange(SCREEN_WIDTH)
            circle_frog.circle_center_y = random.randrange(SCREEN_HEIGHT)
            circle_frog.circle_radius = random.randrange(10, 200)
            circle_frog.circle_angle = random.random() * 2 * math.pi
            self.frog_list.append(circle_frog)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.stars.draw()
        self.skyline1.draw()
        self.skyline2.draw()
        self.player_list.draw()

        self.frog_list.draw()
        self.player_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def update(self, delta_time):
        """ Movement and game logic """
        for frog in self.frog_list:
            if type(frog) is Frog:
                frog.follow_sprite(self.player_sprite)

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.frog_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for frog in hit_list:
            frog.kill()
            self.score += 1

        # Calculate speed based on the keys pressed
        self.skyline1.center_x -= 0.5
        self.skyline2.center_x -= 1
        print(delta_time)
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

        # Call update to move the sprite
        for frog in self.frog_list:
            if type(frog) is BouncingFrog or type(frog) is CircleFrog:
                frog.update()
        # If using a physics engine, call update on it instead of the sprite
        # list.
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
