from abc import ABC, abstractmethod
import solid as sl
import numpy as np
from functools import partialmethod

# base class for all solids
class Solid(ABC):
    @abstractmethod
    def __init__(self):
        pass

    # child __init__() functions responsible for populating self._solid and self._anchors
    def solid(self):
        return self._solid

    def translate(self, x=0, y=0, z=0):
        self._solid = sl.translate([x,y,z])(self._solid)
        self._anchors = utils.translate_points(self._anchors, [x,y,z])

    def rotate(self, x=0, y=0, z=0, degrees=True):
        self._solid = sl.rotate([x, y, z])(self._solid)
        self._anchors = utils.rotate_points(self._anchors, [x,y,z], degrees)

    @abstractmethod
    def anchors(self):
        pass

class Assembly(ABC):
    @abstractmethod
    def __init__(self):
        pass

    # child __init__() functions responsible for populating self._solid and self._anchors
    def solid(self):
        out_solid = None
        for part in self._parts.values():
            out_solid += part.solid()
        return out_solid

    def translate(self, x=0, y=0, z=0):
        self._anchors = utils.translate_points(self._anchors, [x,y,z])
        for part in self._parts.values():
            part.translate(x, y, z)

    def rotate(self, x=0, y=0, z=0, degrees=True):
        self._anchors = utils.rotate_points(self._anchors, [x,y,z], degrees)
        for part in self._parts.values():
            part.rotate(x, y, z)

    def anchors(self, part_name=None):
        # return assembly anchors if no part specified
        if part_name == None:
            return self._anchors
        # return the anchors of the requested part
        return self._parts[part_name].anchors()



class Hull(object):
    def __init__(self, corners):
        """
        sorted corner ordering
           3-------7
          /|      /|
         / |     / | Y
        2--|----6  |
        |  1----|--5
        | /     | / Z
        0-------4
            X
        """
        self.corners = np.array(sorted(corners)).reshape((2,2,2,3))
        self._output_shape = (4,3)

    def _get_side(self, slice):
        coords =  self.corners[slice].reshape(self._output_shape)
        return set(tuple(x) for x in coords)

    right  = partialmethod(_get_side, np.s_[1,:,:])
    left   = partialmethod(_get_side, np.s_[0,:,:])
    top    = partialmethod(_get_side, np.s_[:,1,:])
    bottom = partialmethod(_get_side, np.s_[:,0,:])
    front  = partialmethod(_get_side, np.s_[:,:,1])
    back   = partialmethod(_get_side, np.s_[:,:,0])
