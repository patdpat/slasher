import arcade
import os
import random
import math
import time
from models import *
from background import *

SPRITE_SCALING = 0.25
SPRITE_SCALING_FROG = 0.3
SPRITE_SCALING_HEART = 0.25

FROG_SPEED = 0.75

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "SUCK MY DICK"

MOVEMENT_SPEED = 5
SPRITE_SPEED = 0.5


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
        self.heart_list = None
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
        FROG_COUNT = 70
        BOUNCING_FROG_COUNT = 23
        CIRCLE_FROG_COUNT = 27

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.frog_list = arcade.SpriteList()
        self.heart_list = arcade.SpriteList()
        # Collection variable
        self.score = 0
        # Set up the player part
        self.player_sprite = Player("images/character.png", SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        # Create frog part
        heart = Heart("images/heart.png", SPRITE_SCALING_HEART)
        heart.circle_center_x = random.randrange(SCREEN_WIDTH)
        heart.circle_center_y = random.randrange(SCREEN_HEIGHT)
        heart.circle_radius = random.randrange(10, 200)
        heart.circle_angle = random.random() * 2 * math.pi
        self.heart_list.append(heart)

        for i in range(FROG_COUNT):
            frog_face = random.randint(1, 7)
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

        for i in range(CIRCLE_FROG_COUNT):
            circle_frog = CircleFrog(
                "images/frog/frog9.png", SPRITE_SCALING_FROG)
            circle_frog.circle_center_x = random.randrange(SCREEN_WIDTH)
            circle_frog.circle_center_y = random.randrange(SCREEN_HEIGHT)
            circle_frog.circle_radius = random.randrange(10, 200)
            circle_frog.circle_angle = random.random() * 2 * math.pi
            self.frog_list.append(circle_frog)

    def add_frog(self):
        for i in range(6):
            frog_face = random.randint(1, 7)
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

        for i in range(2):
            bouncing_frog = BouncingFrog(
                "images/frog/frog8.png", SPRITE_SCALING_FROG)
            bouncing_frog.center_x = random.randrange(SCREEN_WIDTH)
            bouncing_frog.center_y = random.randrange(SCREEN_HEIGHT)
            bouncing_frog.change_x = random.randrange(-3, 4)
            bouncing_frog.change_y = random.randrange(-3, 4)
            self.frog_list.append(bouncing_frog)

        for i in range(2):
            circle_frog = CircleFrog(
                "images/frog/frog9.png", SPRITE_SCALING_FROG)
            circle_frog.circle_center_x = random.randrange(SCREEN_WIDTH)
            circle_frog.circle_center_y = random.randrange(SCREEN_HEIGHT)
            circle_frog.circle_radius = random.randrange(10, 200)
            circle_frog.circle_angle = random.random() * 2 * math.pi
            self.frog_list.append(circle_frog)

    def add_heart(self):
        heart = Heart("images/heart.png", SPRITE_SCALING_HEART)
        heart.circle_center_x = random.randrange(SCREEN_WIDTH)
        heart.circle_center_y = random.randrange(SCREEN_HEIGHT)
        heart.circle_radius = random.randrange(10, 200)
        heart.circle_angle = random.random() * 2 * math.pi
        self.heart_list.append(heart)

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()

        # Draw all the sprites.
        self.stars.draw()
        self.skyline1.draw()
        self.skyline2.draw()

        self.player_list.draw()

        self.frog_list.draw()
        self.heart_list.draw()
        self.player_list.draw()

        # Put the text on the screen.
        # output = f"Level: {self.level}"
        # arcade.draw_text(output, 10, 35, arcade.color.WHITE, 15)
        output = f"NUMBER OF CURRENT FROG: {len(self.frog_list)}"
        arcade.draw_text(output, 10, 80, arcade.color.WHITE, 18)
        output = f"YOU ALREADY HIT    :  {self.score} FROGS "
        arcade.draw_text(output, 10, 50, arcade.color.RED, 18)
        output = f"!!!WARNING!!! EVERY 5 FROG YOU HIT YOU'LL GET 10 MORE"
        arcade.draw_text(output, 10, 20, arcade.color.RED, 18)

    def update(self, delta_time):
        """ Movement and game logic """
        for frog in self.frog_list:
            if type(frog) is Frog:
                frog.follow_sprite(self.player_sprite)
        # Call update to move the sprite
        for frog in self.frog_list:
            if type(frog) is BouncingFrog or type(frog) is CircleFrog:
                frog.update()

        for heart in self.heart_list:
            heart.update()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.frog_list)
        next_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.heart_list)
        # Loop through each colliding sprite, remove it, and add to the score.
        for frog in hit_list:
            frog.kill()
            self.score += 1


  

# TODO
        for heart in next_list:
            heart.kill()
            for i in range(5):
                target = random.randint(1, len(self.frog_list)-1)
                self.frog_list[target].kill()
            self.add_heart()

        # Calculate speed based on the keys pressed
        self.skyline1.center_x -= 0.5
        self.skyline2.center_x -= 1
        # print(delta_time)
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
