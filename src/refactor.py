import solid as sl
from pathlib import Path
import configparser

# within project
import Socket

config = configparser.ConfigParser()
config.read('default_config.ini')

intermediates_dir = Path.cwd().parent / "intermediates"
intermediates_dir.mkdir(exist_ok=True)

# key switch socket
socket = Socket.CherryMXSocket(config['socket'])
socket_output = intermediates_dir / "socket.scad"
sl.scad_render_to_file(socket.solid(), socket_output)

# key caps
