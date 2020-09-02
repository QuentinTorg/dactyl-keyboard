import solid as sl
from pathlib import Path
import configparser

# within project
import switch_socket
import keycap

config = configparser.ConfigParser()
config.read('default_config.ini')

intermediates_dir = Path(__file__).resolve().parent.parent / 'intermediates'
intermediates_dir.mkdir(exist_ok=True)

# key switch socket
socket = switch_socket.CherryMXSocket(config['socket'])
socket_output = intermediates_dir / 'socket.scad'
sl.scad_render_to_file(socket.solid(), socket_output)

# key cap
keycapsolid = keycap.OEM(1,1).solid()
for r in range(2, 5):
    keycapsolid = sl.translate([0, 19, 0])(keycapsolid)
    keycapsolid += keycap.OEM(r,1).solid()
keycap_output = intermediates_dir / 'keycaps.scad'
sl.scad_render_to_file(keycapsolid, keycap_output)

# key caps
