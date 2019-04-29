import arcade
import os
import random
import math
import time
from models import *


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
