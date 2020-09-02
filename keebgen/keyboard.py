from .geometry_base import Assembly

class Keyboard(Assembly):
    def __init__(self, parts, anchors):
        if type(self) is Keyboard:
            raise Exception(f'{self.__class__.__name__} is an abstract class and cannot be instantiated directly.')
        super().__init__(parts, anchors)


class DactylManuform(Keyboard):
    def __init__(self, rows=4, cols=5):
        #TODO: add everything
        super().__init__({}, {})

