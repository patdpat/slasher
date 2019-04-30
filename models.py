import random
import arcade
import math
import os

SPRITE_SCALING = 0.25
SPRITE_SCALING_FROG = 0.3
SPRITE_SCALING_HEART = 0.25

FROG_SPEED = 0.75

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "JUKE DA FROG"

MOVEMENT_SPEED = 5
SPRITE_SPEED = 0.5

# TODO NO DEATH IF YOU HIT MORE FROG NEXT ROUND YOU GET MORE FRONG AS PENALTY


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


class Heart(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.circle_angle = 0

        self.circle_radius = 0

        self.circle_speed = 0.008

        self.circle_center_x = 0
        self.circle_center_y = 0

    def update(self):

        self.center_x = self.circle_radius * math.sin(self.circle_angle) \
            + self.circle_center_x
        self.center_y = self.circle_radius * math.cos(self.circle_angle) \
            + self.circle_center_y

        self.circle_angle += self.circle_speed


class BouncingFrog(arcade.Sprite):

    # This class represent frog that bounce around

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0

    def update(self):

        # Move frog
        self.center_x += self.change_x
        self.center_y += self.change_y

        # If frog hti rim then make it bounce
        if self.left < 0:
            self.change_x *= -1

        if self.right > SCREEN_WIDTH:
            self.change_x *= -1

        if self.bottom < 0:
            self.change_y *= -1

        if self.top > SCREEN_HEIGHT:
            self.change_y *= -1


class Frog(arcade.Sprite):
    """
    This class represents frog that directly chase toward player 
    """

    def follow_sprite(self, player_sprite):
        """
        This function will move the frog toward player
        """

        self.center_x += self.change_x
        self.center_y += self.change_y

        if random.randrange(100) == 0:
            start_x = self.center_x
            start_y = self.center_y

            # find the destination of player
            dest_x = player_sprite.center_x
            dest_y = player_sprite.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # calculate angle of attack
            self.change_x = math.cos(angle) * FROG_SPEED
            self.change_y = math.sin(angle) * FROG_SPEED


class CircleFrog(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.circle_angle = 0

        self.circle_radius = 0

        self.circle_speed = 0.008

        self.circle_center_x = 0
        self.circle_center_y = 0

    def update(self):

        self.center_x = self.circle_radius * math.sin(self.circle_angle) \
            + self.circle_center_x
        self.center_y = self.circle_radius * math.cos(self.circle_angle) \
            + self.circle_center_y

        self.circle_angle += self.circle_speed
