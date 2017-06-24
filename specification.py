

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


class PenguinSpec:
    def __init__(self, spec_dict):
        self.movevel = spec_dict["move_velocity"]
        self.radius = spec_dict["radius"]
        self.mass = spec_dict["mass"]
        self.stuntmax = spec_dict["stun_timer_max"]
        self.pngindmax = spec_dict["pushing_index_max"]
        self.pngvel = spec_dict["pushing_velocity"]
        self.pngtmax = spec_dict["pushing_timer_max"]
        self.sbtimermax = spec_dict["snowball_timer_max"]


class SnowballSpec:
    def __init__(self, spec_dict):
        self.radius = spec_dict["radius"]
        self.mass = spec_dict["mass"]
        self.flyvel = spec_dict["fly_velocity"]
