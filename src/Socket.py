import solid as sl

import TransformUtils

# top, bottom, left, right are relative to the user sitting at the keyboard

class CherryMX:
    def __init__(self, config):
        width = config.getfloat('overall_width')
        height = config.getfloat('overall_height')
        switch_height = config.getfloat('keyswitch_width')  ## Was 14.1, then 14.25
        switch_width = config.getfloat('keyswitch_width')
        thickness = config.getfloat('plate_thickness')
        hot_swap = config.getboolean('hot_swap')

        # parameters not pulled from config file
        # most people should not need to modify these
        side_nub_width = 2.75
        side_nub_radius = 1.0
        cylinder_segments = 25

        # calculated numbers
        border_width = (width - switch_width) / 2
        border_height = (height - switch_height) / 2


        ### Make Geometry ###
        # make two of the four walls, b/c rotationally symmetric
        top_wall = sl.cube([width, border_height, thickness], center=True)
        top_wall = sl.translate([0, (border_height + switch_height)/2, thickness/2])(top_wall)

        right_wall = sl.cube([border_width, height, thickness], center=True)
        right_wall = sl.translate([(border_width + switch_width)/2, 0, thickness/2])(right_wall)

        # tapered side nub that stabilizes the switch, goes in right wall
        side_nub = sl.cylinder(side_nub_radius, side_nub_width, segments=cylinder_segments, center=True)
        side_nub = sl.rotate(90, [1, 0, 0])(side_nub)
        side_nub = sl.translate([switch_width/2, 0, 1])(side_nub)
        nub_cube = sl.cube([border_width, side_nub_width, thickness], center=True)
        nub_cube = sl.translate([(border_width + switch_width)/2, 0, thickness/2])(nub_cube)
        side_nub = sl.hull()(side_nub, nub_cube)

        # use rotational symmetry to make full socket
        socket_half = top_wall + right_wall + side_nub
        socket = socket_half + sl.rotate(180, [0, 0, 1])(socket_half)

        # add hot swap socket
        # todo, configure for different hot swap socket types
        if hot_swap:
            #TODO: fix the hot swap socket. currently not parameterized
            # missing the stl file in this repo

            hot_swap_socket = sl.import_(path.join(r"..", "geometry", r"hot_swap_plate.stl"))
            hot_swap_socket = sl.translate([0, 0, thickness - 5.25])(hot_swap_socket)
            socket = sl.union()(socket, hot_swap_socket)

        self.__socket = socket

        # corners start in top left, then work their way around
        #
        top_z = thickness
        bottom_z = 0.0
        half_width = width/2
        half_height = height/2
        self.__corners = [[-half_width,  half_height, top_z],
                        [ half_width,  half_height, top_z],
                        [ half_width, -half_height, top_z],
                        [-half_width, -half_height, top_z],
                        [-half_width,  half_height, bottom_z],
                        [ half_width,  half_height, bottom_z],
                        [ half_width, -half_height, bottom_z],
                        [-half_width, -half_height, bottom_z]]

    def solid(self):
        return self.__socket

    def translate(self, x=0, y=0, z=0):
        self.__socket = sl.translate([x,y,z])(self.__socket)
        self.__corners = TransformUtils.translate_points(self.__corners, [x,y,z])

    def rotate(self, x=0, y=0, z=0, degrees=True):
        self.__socket = sl.rotate([x, y, z])(self.__socket)
        self.__corners = TransformUtils.rotate_points(self.__corners, [x,y,z], degrees)

    def corners(self):
        c = {}
        c['upper_top_left'] = self.__corners[0]
        c['upper_top_right'] = self.__corners[1]
        c['upper_bottom_right'] = self.__corners[2]
        c['upper_bottom_left'] = self.__corners[3]
        c['lower_top_left'] = self.__corners[4]
        c['lower_top_right'] = self.__corners[5]
        c['lower_bottom_right'] = self.__corners[6]
        c['lower_bottom_left'] = self.__corners[7]
        return c
