from abc import ABC, abstractmethod
import solid as sl

import TransformUtils as utils


class Keyboard(ABC):
    def __init__(self):
        if type(self) is Keyboard:
            raise Exception(f'{self.__class__.__name__} is an abstract class and cannot be instantiated directly.')


class DactylManuform(Keyboard):
    def __init__(self):
        super(DactylManuform, self).__init__()


