import arcade
import os
import random
import math
import time
from models import *
from background import *
INSTRUCTIONS_PAGE_0 = 0
INSTRUCTIONS_PAGE_1 = 1
GAME_RUNNING = 2
GAME_OVER = 3
GAME_WIN = 4
SPRITE_SCALING = 0.25
SPRITE_SCALING_FROG = 0.3
SPRITE_SCALING_HEART = 0.25

FROG_SPEED = 0.75

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "SLASHER : JUKE THE FROG"

MOVEMENT_SPEED = 5
SPRITE_SPEED = 0.5


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
        self.current_state = INSTRUCTIONS_PAGE_0
        self.instructions = []
        texture = arcade.load_texture("images/instructions_0.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("images/instructions_1.png")
        self.instructions.append(texture)

        # Variables that will hold sprite lists
        self.player_list = None
        self.frog_list = None
        self.heart_list = None
        # Set up the player info
        self.player_sprite = None
        self.should_add = 0

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(True)

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game and initialize the variables. """
        FROG_COUNT = 75
        BOUNCING_FROG_COUNT = 25
        CIRCLE_FROG_COUNT = 30

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

    def draw_instructions_page(self, page_number):
        """
        Draw an instruction page. Load the page as an image.
        """
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)

    def draw_game_win(self):
        """
        Draw "Game winr" across the screen.
        """
        output = "You  Wins "
        arcade.draw_text(output, 240, 600, arcade.color.WHITE, 54)
        output = "NUMBER OF FROG IS LESS THAN 5"
        arcade.draw_text(output, 80, 500, arcade.color.WHITE, 34)
        output = f"THIS ROUND YOU HITS {self.score} FROGS"
        arcade.draw_text(output, 70, 400, arcade.color.RED, 34)
        output = "Click to restart"
        arcade.draw_text(output, 310, 200, arcade.color.WHITE, 24)

    def draw_game_over(self):
        """
        Draw "Game over" across the screen.
        """
        output = "Game Over "
        arcade.draw_text(output, 240, 600, arcade.color.WHITE, 54)
        output = "NUMBER OF FROG EXCEED 200"
        arcade.draw_text(output, 110, 500, arcade.color.WHITE, 34)
        output = f"THIS ROUND YOU HITS {self.score} FROGS"
        arcade.draw_text(output, 70, 400, arcade.color.RED, 34)
        output = "Click to restart"
        arcade.draw_text(output, 310, 200, arcade.color.WHITE, 24)

    def add_frog(self):
        for i in range(4):
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

        for i in range(1):
            bouncing_frog = BouncingFrog(
                "images/frog/frog8.png", SPRITE_SCALING_FROG)
            bouncing_frog.center_x = random.randrange(SCREEN_WIDTH)
            bouncing_frog.center_y = random.randrange(SCREEN_HEIGHT)
            bouncing_frog.change_x = random.randrange(-3, 4)
            bouncing_frog.change_y = random.randrange(-3, 4)
            self.frog_list.append(bouncing_frog)

        for i in range(1):
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

    def draw_game(self):
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
        output = f"NUMBER OF CURRENT FROG: {len(self.frog_list)} "
        arcade.draw_text(output, 10, 110, arcade.color.WHITE, 18)
        output = f"YOU'LL LOSE IF CURRENT FROG EXCEED 200"
        arcade.draw_text(output, 10, 80, arcade.color.WHITE, 18)
        output = f"YOU ALREADY HIT    :  {self.score} FROGS "
        arcade.draw_text(output, 10, 50, arcade.color.RED, 18)
        output = f"EVERY 5 FROGS YOU HIT YOU'LL GET 6 MORE"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 18)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        if self.current_state == INSTRUCTIONS_PAGE_0:
            self.draw_instructions_page(0)

        elif self.current_state == INSTRUCTIONS_PAGE_1:
            self.draw_instructions_page(1)

        elif self.current_state == GAME_RUNNING:
            self.draw_game()
        else:
            if self.current_state == GAME_WIN:
                self.draw_game_win()
            else:
                self.draw_game_over()

    def update(self, delta_time):
        # Only move and do things if the game is running.
        if self.current_state == GAME_RUNNING:
            # Call update on all sprites (The sprites don't do much in this

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
            # Loop through each colliding sprite, remove it, and add to the hit.
            for frog in hit_list:
                which_sound = random.randint(1, 4)
                if which_sound == 1:
                    arcade.Sound("sounds/frog.mp3").play()
                elif which_sound == 2:
                    arcade.Sound("sounds/work.mp3").play()
                elif which_sound == 3:
                    arcade.Sound("sounds/work2.mp3").play()
                elif which_sound == 4:
                    arcade.Sound("sounds/work3.mp3").play()
                frog.kill()
                self.score += 1
                self.should_add += 1
    # TODO  #Game Logic and ETC.
            for heart in next_list:
                arcade.Sound("sounds/heart.mp3").play()
                heart.kill()
                for i in range(5):
                    target = random.randint(1, len(self.frog_list)-1)
                    self.frog_list[target].kill()
                self.add_heart()

            if self.should_add > 5:
                self.add_frog()
                self.should_add -= 5

            if len(self.frog_list) > 200:
                arcade.Sound("sounds/lose.mp3").play()
                self.current_state = GAME_OVER
# TODO Fix win sounds
            if len(self.frog_list) <= 5:
                arcade.Sound("sounds/win.mp3").play()
                self.current_state = GAME_WIN

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

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Change states as needed.
        if self.current_state == INSTRUCTIONS_PAGE_0:
            # Next page of instructions.
            self.current_state = INSTRUCTIONS_PAGE_1
        elif self.current_state == INSTRUCTIONS_PAGE_1:
            # Start the game
            self.setup()
            self.current_state = GAME_RUNNING
        elif self.current_state == GAME_OVER:
            # Restart the game.
            self.setup()
            self.current_state = GAME_RUNNING
        elif self.current_state == GAME_WIN:
            # Restart the game.
            self.setup()
            self.current_state = GAME_RUNNING


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
