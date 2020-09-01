from abc import ABC, abstractmethod
import solid as sl
from pathlib import Path

import transform_utils as utils
from geometry_base import Solid

# top, bottom, left, right are relative to the user sitting at the keyboard

# Socket is an abstract class that represents all implemented socket types
# self.__corners list must contain the outer corner locations of the socket. The order starting
#     with top face, rotating from top left around socket clockwise, then bottom face, rotating
#     from top left around the socket clockwise
# self.__socket is the solidpython object
class Socket(Solid):
    @abstractmethod
    def __init__(self, solid, corners):
        if type(self) is Socket:
            raise Exception(f'{self.__class__.__name__} is an abstract class and cannot be instantiated directly.')
        self.__solid = solid
        self.__corners = corners
        super(Socket, self).__init__(self.__solid, self.__corners)

    def corners(self):
        #TODO this is not finalized output format yet
        # maybe need to apply multiple groups of corners
        # only returns the current corner locations
        c = {}
        c['top'] = set([
            self.__corners[0],
            self.__corners[1],
            self.__corners[2],
            self.__corners[3]])
        c['bottom'] = set([
            self.__corners[4],
            self.__corners[5],
            self.__corners[6],
            self.__corners[7]])
        c['left'] = set([
            self.__corners[0],
            self.__corners[3],
            self.__corners[4],
            self.__corners[7]])
        c['right'] = set([
            self.__corners[1],
            self.__corners[2],
            self.__corners[5],
            self.__corners[6]])
        c['front'] = set([
            self.__corners[0],
            self.__corners[1],
            self.__corners[4],
            self.__corners[5]])
        c['back'] = set([
            self.__corners[2],
            self.__corners[3],
            self.__corners[6],
            self.__corners[7]])
        return c


class CherryMXSocket(Socket):
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
        # TODO, configure for different hot swap socket types
        if hot_swap:
            #TODO: fix the hot swap socket. currently not parameterized
            # missing the stl file in this repo

            hot_swap_socket = sl.import_(Path.cwd().parent / "geometry" / "hot_swap_plate.stl")
            hot_swap_socket = sl.translate([0, 0, thickness - 5.25])(hot_swap_socket)
            socket = sl.union()(socket, hot_swap_socket)

        self.__solid = socket

        # corners start in top left, then work their way around
        #
        top_z = thickness
        bottom_z = 0.0
        half_width = width/2
        half_height = height/2
        # self.__corners must be loaded in this order
        self.__corners = [[-half_width,  half_height, top_z],
                          [ half_width,  half_height, top_z],
                          [ half_width, -half_height, top_z],
                          [-half_width, -half_height, top_z],
                          [-half_width,  half_height, bottom_z],
                          [ half_width,  half_height, bottom_z],
                          [ half_width, -half_height, bottom_z],
                          [-half_width, -half_height, bottom_z]]

        # set the base class parameters
        super(CherryMXSocket, self).__init__(self.__solid, self.__corners)
