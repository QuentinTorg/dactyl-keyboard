import solid as sl
import numpy as np
from numpy import pi
import os.path as path
import configparser
from pathlib import Path

# within project
import Socket

config = configparser.ConfigParser()
config.read('default_config.ini')

# parents[0] returns current dir, parents[1] returns one level higher
intermediates_dir = Path(__file__).resolve().parents[1] / "intermediates"
intermediates_dir.mkdir(parents=True, exist_ok=True)

# key switch socket
socket = Socket.CherryMXSocket(config['socket'])
socket_output = intermediates_dir / "socket.scad"
sl.scad_render_to_file(socket.solid(), socket_output)

# key caps
