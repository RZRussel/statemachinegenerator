from nusmv.expression_builder import *
from nusmv.specification import *


class SnowballGenerator:
    def __init__(self, specification):
        self.specification = specification

    def flew(self):
        pass

    def collision_detected(self):
        pass

    def dead_point_reached(self):
        pass


class PenguinGenerator:
    def __init__(self, specification):
        self.specification = specification

    def moved(self):
        pass

    def snowball_initialized(self):
        pass

    def flashed(self):
        pass

    def pushed(self):
        pass

    def pushed_initial_index(self):
        pass

    def static_collision_initialized(self):
        pass

    def flashing_collision_initialized(self):
        pass

    def collision_detected(self):
        pass

    def dead_point_reached(self):
        pass
