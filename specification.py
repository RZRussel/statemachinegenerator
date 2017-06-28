import math

class WorldSpec:
    def __init__(self, spec_dict):
        self.maxx = spec_dict["max_x"]
        self.maxy = spec_dict["max_y"]


class IslandSpec:
    def __init__(self, spec_dict):
        self.centerx = spec_dict["center_x"]
        self.centery = spec_dict["center_y"]
        self.sradius = spec_dict["small_radius"]
        self.bradius = spec_dict["big_radius"]
        self.friction = spec_dict["friction"]

    def getlfocus(self):
        return (self.centerx - math.sqrt(self.bradius*self.bradius - self.sradius*self.sradius), self.centery)

    def getrfocus(self):
        return (self.centerx + math.sqrt(self.bradius * self.bradius - self.sradius * self.sradius), self.centery)

    def contains(self, point):
        lf = self.getlfocus()
        rf = self.getrfocus()
        d1 = math.sqrt((lf[0] - point[0])*(lf[0] - point[0]) + (lf[1] - point[1])*(lf[1] - point[1]))
        d2 = math.sqrt((rf[0] - point[0])*(rf[0] - point[0]) + (rf[1] - point[1])*(rf[1] - point[1]))
        return d1 + d2 <= 2*self.bradius


class PenguinSpec:
    def __init__(self, spec_dict):
        self.movevel = spec_dict["move_velocity"]
        self.radius = spec_dict["radius"]
        self.mass = spec_dict["mass"]
        self.pngvel = spec_dict["pushing_velocity"]
        self.sbox = spec_dict["snowball_ox"]
        self.sboy = spec_dict["snowball_oy"]

class SnowballSpec:
    def __init__(self, spec_dict):
        self.radius = spec_dict["radius"]
        self.mass = spec_dict["mass"]
        self.flyvel = spec_dict["fly_velocity"]
