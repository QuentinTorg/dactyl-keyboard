from abc import ABC, abstractmethod
import solid as sl

import transform_utils as utils
from geometry_base import Assembly
import switch_socket
import keycap

# different Key subclasses will exist depending on the desired alignment
# alignment is driven by where the anchor points are placed
class Key(Assembly):
    # a Key represents the socket and keycap together,
    # this allows sockets to be arranged differently on a board depending on keycap geometry

    # TODO the config shoud have the socket_config nested within it eventaully
    @abstractmethod
    def __init__(self, config, socket_config, r, u=1):
        if type(self) is Key:
            raise Exception(f'{self.__class__.__name__} is an abstract class and cannot be instantiated directly.')

        # this will hold all parts of the key
        self.__parts = {}
        if config.get('switch_type') == 'cherry_mx':
            self.__parts['socket'] = switch_socket.CherryMXSocket(socket_config, u)
        else:
            raise Exception('socket for switch type ' + config.get('switch_type') + ' not implemented')

        if config.get('keycap_type') == 'oem':
            self.__parts['keycap'] = keycap.OEM(r, u)
        else:
            raise Exception('keycap type ' + config.get('keycap_type') + ' not implemented')

        # if created correclty, the key switch and key cap should already be aligned to each other
        super(Key, self).__init__(self.__parts, self.__anchors)


# FaceAlignedKeys will have the faces forming a smooth curve on the keybaord regardless of switch and keycap type
class FaceAlignedKey(Key)
    def __init__(self, config, socket_config, r, u=1):
        # this will load the self.__parts dict according to config
        super(FaceAlignedKey, self).__init__(config, socket_config, r, u)
        # set the assembly corner anchors to top of the socket
        self.__anchors = self.anchors('keycap')['top']

        # reorient the key and switch together so the top face of the keycap is centered
        # on the z axis and coplanar with the xy plane

        # assumes a symmetrical keycap from left to right




# simplest case, the switches are aligned based on the socket.
# should be used for plate mount boards
class SocketAlignedKey(Key)
    def __init__(self, config, socket_config, r, u=1):
        # this will load the self.__parts dict according to config
        super(FaceAlignedKey, self).__init__(config, socket_config, r, u)

        # set the assembly corner anchors to top of the socket
        self.__anchors = anchors('socket')['top']
        # no additional alignment required
