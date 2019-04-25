import arcade
import os
import random
import math
import time

SPRITE_SCALING = 0.1
SPRITE_SCALING_COIN = 0.3
COIN_COUNT = 40
COIN_SPEED = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "GU MAI AOW LEAW AI SU"

MOVEMENT_SPEED = 5
SPRITE_SPEED = 0.5
def make_star_field(star_count):
    """ Make a bunch of circles for stars. """

    shape_list = arcade.ShapeElementList()

    for star_no in range(star_count):
        x = random.randrange(SCREEN_WIDTH)
        y = random.randrange(SCREEN_HEIGHT)
        radius = random.randrange(1, 4)
        brightness = random.randrange(127, 256)
        color = (brightness, brightness, brightness)
        shape = arcade.create_ellipse_filled(x, y, radius, radius, color, num_segments=8)
        shape_list.append(shape)

    return shape_list


def make_skyline(width, skyline_height, skyline_color,
                 gap_chance = 0.70, window_chance=0.30, light_on_chance=0.5,
                 window_color=(255, 255, 200), window_margin=3, window_gap=2,
                 cap_chance=0.20):
    """ Make a skyline """

    shape_list = arcade.ShapeElementList()

    # Add the "base" that we build the buildings on
    shape = arcade.create_rectangle_filled(width / 2, skyline_height / 2, width, skyline_height, skyline_color)
    shape_list.append(shape)

    building_center_x = 0
    while building_center_x < width:

        # Is there a gap between the buildings?
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

            shape = arcade.create_polygon([[x1, y1], [x2, y2], [x3, y3]], skyline_color)
            shape_list.append(shape)

        # See if we should have some windows
        if random.random() < window_chance:
            # Yes windows! How many windows?
            window_rows = random.randrange(10, 15)
            window_columns = random.randrange(1, 7)

            # Based on that, how big should they be?
            window_height = (building_height - window_margin * 2) / window_rows
            window_width = (building_width - window_margin * 2 - window_gap * (window_columns - 1)) / window_columns

            # Find the bottom left of the building so we can start adding widows
            building_base_y = building_center_y - building_height / 2
            building_left_x = building_center_x - building_width / 2

            # Loop through each window
            for row in range(window_rows):
                for column in range(window_columns):
                    if random.random() < light_on_chance:
                        window_y = building_base_y + row * window_height + window_height / 2
                        window_x = building_left_x + column * (window_width + window_gap) + window_width / 2 + window_margin
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

class Coin(arcade.Sprite):
    """
    This class represents the coins on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    def follow_sprite(self, player_sprite):
        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.

        We use the 'min' function here to get the sprite to line up with
        the target sprite, and not jump around if the sprite is not off
        an exact multiple of SPRITE_SPEED.
        """

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Random 1 in 100 chance that we'll change from our old direction and
        # then re-aim toward the player
        if random.randrange(100) == 0:
            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the bullet
            dest_x = player_sprite.center_x
            dest_y = player_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            self.change_x = math.cos(angle) * COIN_SPEED
            self.change_y = math.sin(angle) * COIN_SPEED



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
        self.coin_list = None
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
        self.coin_list = arcade.SpriteList()

        # Score
        self.score = 0


        # Set up the player
        self.player_sprite = Player("images/character.png", SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        # Create the coins
        for i in range(COIN_COUNT):

            # Create the coin instance
            frog_face = random.randint(1,8)
            if frog_face == 1:
                coin = Coin("images/frog/frog1.png", SPRITE_SCALING_COIN)
            if frog_face == 2:
                coin = Coin("images/frog/frog2.png", SPRITE_SCALING_COIN)
            if frog_face == 3:
                coin = Coin("images/frog/frog3.png", SPRITE_SCALING_COIN)
            if frog_face == 4:
                coin = Coin("images/frog/frog4.png", SPRITE_SCALING_COIN)
            if frog_face == 5:
                coin = Coin("images/frog/frog5.png", SPRITE_SCALING_COIN)
            if frog_face == 6:
                coin = Coin("images/frog/frog6.png", SPRITE_SCALING_COIN)
            if frog_face == 7:
                coin = Coin("images/frog/frog7.png", SPRITE_SCALING_COIN)
            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)
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

        self.coin_list.draw()
        self.player_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        

    def update(self, delta_time):
        """ Movement and game logic """
        for coin in self.coin_list:
            coin.follow_sprite(self.player_sprite)

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            coin.kill()
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