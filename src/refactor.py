import solid as sl
import numpy as np
from numpy import pi
import os.path as path
import configparser

# within project
import Socket

config = configparser.ConfigParser()
config.read('default_config.ini')

socket = Socket.CherryMX(config['socket'])

sl.scad_render_to_file(socket.solid(), path.join(r"..", "things", r"testing.scad"))
