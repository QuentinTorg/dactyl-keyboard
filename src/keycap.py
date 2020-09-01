from abc import ABC, abstractmethod
import solid as sl
import numpy as np
import itertools


class Keycap(ABC):
    def __init__(self):
        if type(self) is Keycap:
            raise Exception(f'{self.__class__.__name__} is an abstract class and cannot be instantiated directly.')

class OEM(Keycap):
    pass

class SA(Keycap):
    def __init__(self, num_units=1):
        self.num_units = num_units


