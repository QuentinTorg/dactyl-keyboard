from abc import ABC, abstractmethod
import solid as sl
from pathlib import Path

import keebgen.transform_utils as utils
from keebgen.geometry_base import Solid

# top, bottom, left, right are relative to the user sitting at the keyboard

# Socket is an abstract class that represents all implemented socket types
# self._anchors list must contain the outer corner locations of the socket. The order starting
#     with top face, rotating from top left around socket clockwise, then bottom face, rotating
#     from top left around the socket clockwise
# self.__socket is the solidpython object
class Socket(Solid):
    # when adding new sockets, the top of the socket should be coplanar with the X,Y plane
    # when the switch is installed, the keycap mounting feature should align with the Z axis
    @abstractmethod
    def __init__(self):
        super(Socket, self).__init__()

    def anchors(self):
        #TODO this is not finalized output format yet
        # maybe need to apply multiple groups of anchors
        # only returns the current corner locations
        c = {}
        c['top'] = set([
            self._anchors[0],
            self._anchors[1],
            self._anchors[2],
            self._anchors[3]])
        c['bottom'] = set([
            self._anchors[4],
            self._anchors[5],
            self._anchors[6],
            self._anchors[7]])
        c['left'] = set([
            self._anchors[0],
            self._anchors[3],
            self._anchors[4],
            self._anchors[7]])
        c['right'] = set([
            self._anchors[1],
            self._anchors[2],
            self._anchors[5],
            self._anchors[6]])
        c['front'] = set([
            self._anchors[0],
            self._anchors[1],
            self._anchors[4],
            self._anchors[5]])
        c['back'] = set([
            self._anchors[2],
            self._anchors[3],
            self._anchors[6],
            self._anchors[7]])
        return c


class CherryMXSocket(Socket):
    def __init__(self, config, u=1):
        super(CherryMXSocket, self).__init__()
        # determines how much flat space to reserve around the switch
        # prevents interference between keycap and other geometry
        width = config.getfloat('overall_width') + (u-1) * 19.0
        length = config.getfloat('overall_length')
        # changes how tight of a fit the switch is in the opening
        switch_length = config.getfloat('switch_opening_length')  ## Was 14.1, then 14.25
        switch_width = config.getfloat('switch_opening_width')
        # plate thickness for where the switch plugs in
        thickness = config.getfloat('plate_thickness')
        # if using hot swap PCB's. This is not currently implemented
        add_hot_swap = config.getboolean('hot_swap')
        add_side_nubs = config.getboolean('side_nubs')

        # parameters not pulled from config file
        # most people should not need to modify these
        side_nub_width = 2.75
        side_nub_radius = 1.0

        ### Make Geometry ###
        # make two of the four walls, b/c rotationally symmetric
        socket = sl.cube([width, length, thickness], center=True)
        socket -= sl.cube([switch_width, switch_length, thickness*2], center=True)
        socket = sl.translate([0, 0, -thickness/2])(socket)

        # tapered side nub that stabilizes the switch, goes in right wall
        if add_side_nubs:
            side_nub = sl.cylinder(side_nub_radius, side_nub_width, segments=20, center=True)
            side_nub = sl.rotate(90, [1, 0, 0])(side_nub)
            side_nub = sl.translate([switch_width/2, 0, side_nub_radius-thickness])(side_nub)
            nub_cube_len = (width-switch_width)/2
            nub_cube = sl.cube([nub_cube_len, side_nub_width, thickness], center=True)
            nub_cube = sl.translate([(width-nub_cube_len)/2, 0, -thickness/2])(nub_cube)
            side_nub = sl.hull()(side_nub, nub_cube)

            socket += side_nub + sl.rotate([0, 0, 180])(side_nub)

        # add hot swap socket
        # TODO, configure for different hot swap socket types
        if add_hot_swap:
            #TODO: fix the hot swap socket. currently not parameterized
            # missing the stl file in this repo
            raise Exception('hot swap sockets are not yet implemented')

            hot_swap_socket = sl.import_(Path.cwd().parent / "geometry" / "hot_swap_plate.stl")
            hot_swap_socket = sl.translate([0, 0, thickness - 5.25])(hot_swap_socket)
            socket = sl.union()(socket, hot_swap_socket)

        self._solid = socket

        # anchors start in top left, then work their way around
        #
        top_z = 0.0
        bottom_z = -thickness
        half_width = width/2.0
        half_length = length/2.0
        # self._anchors must be loaded in this order
        self._anchors = [[-half_width,  half_length, top_z],
                          [ half_width,  half_length, top_z],
                          [ half_width, -half_length, top_z],
                          [-half_width, -half_length, top_z],
                          [-half_width,  half_length, bottom_z],
                          [ half_width,  half_length, bottom_z],
                          [ half_width, -half_length, bottom_z],
                          [-half_width, -half_length, bottom_z]]
