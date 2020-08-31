import solid as sl
import numpy as np
#import configparser

# top, bottom, left, right are relative to the user sitting at the keyboard

class CherryMX:
    def __init__(self, config):
        self.width = config.getfloat('overall_width')
        self.height = config.getfloat('overall_height')
        self.switch_height = config.getfloat('keyswitch_width')  ## Was 14.1, then 14.25
        self.switch_width = config.getfloat('keyswitch_width')
        self.thickness = config.getfloat('plate_thickness')
        self.hot_swap = config.getboolean('hot_swap')

        # generally constant parameters, not pulled from config file
        self.side_nub_width = 2.75
        self.side_nub_radius = 1.0

        # calculated numbers
        self.border_width = (self.width - self.switch_width) / 2
        self.border_height = (self.height - self.switch_height) / 2

    def solid(self, cylinder_segments=100):
        # make two of the four walls, b/c rotationally symmetric
        top_wall = sl.cube([self.width, self.border_height, self.thickness], center=True)
        top_wall = sl.translate([0, (self.border_height + self.switch_height)/2, self.thickness/2])(top_wall)

        right_wall = sl.cube([self.border_width, self.height, self.thickness], center=True)
        right_wall = sl.translate([(self.border_width + self.switch_width)/2, 0, self.thickness/2])(right_wall)

        # tapered side nub that stabilizes the switch, goes in right wall
        side_nub = sl.cylinder(self.side_nub_radius, self.side_nub_width, segments=cylinder_segments, center=True)
        side_nub = sl.rotate(90, [1, 0, 0])(side_nub)
        side_nub = sl.translate([self.switch_width/2, 0, 1])(side_nub)
        nub_cube = sl.cube([self.border_width, self.side_nub_width, self.thickness], center=True)
        nub_cube = sl.translate([(self.border_width + self.switch_width)/2, 0, self.thickness/2])(nub_cube)
        side_nub = sl.hull()(side_nub, nub_cube)

        # use rotational symmetry to make full plate
        plate_half = top_wall + right_wall + side_nub
        plate = plate_half + sl.rotate(180, [0, 0, 1])(plate_half)

        # add hot swap socket
        # todo, configure for different hot swap socket types
        if self.hot_swap:
            #TODO: fix the hot swap socket. currently not parameterized
            # missing the stl file in this repo

            hot_swap_socket = sl.import_(path.join(r"..", "geometry", r"hot_swap_plate.stl"))
            hot_swap_socket = sl.translate([0, 0, self.thickness - 5.25])(hot_swap_socket)

            plate = sl.union()(plate, hot_swap_socket)

        return plate
