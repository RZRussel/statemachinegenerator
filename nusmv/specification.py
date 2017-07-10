import yaml


class World:
    def __init__(self, max_x, max_y):
        if type(max_x) != int:
            raise TypeError("Expected int type for max_x")

        if type(max_y) != int:
            raise TypeError("Expected int type for max_y")

        self.max_x = max_x
        self.max_y = max_y


class Island:
    def __init__(self, center_x, center_y, small_radius, big_radius):
        if type(center_x) != int:
            raise TypeError("Expected int type for center_x")

        if type(center_y) != int:
            raise TypeError("Expected int type for center_y")

        if type(small_radius) != int:
            raise TypeError("Expected int type for small_radius")

        if type(big_radius) != int:
            raise TypeError("Expected int type for big_radius")

        self.center_x = center_x
        self.center_y = center_y
        self.small_radius = small_radius
        self.big_radius = big_radius


class Penguin:
    def __init__(self, radius, move_velocity, flash_velocity, sliding_friction, snowball_ox, snowball_oy):
        if type(radius) != int:
            raise TypeError("Expected int type for radius")

        if type(move_velocity) != int:
            raise TypeError("Expected int type for move_velocity")

        if type(flash_velocity) != int:
            raise TypeError("Expected int type for flash_velocity")

        if type(sliding_friction) != int:
            raise TypeError("Expected int type for sliding_friction")

        if type(snowball_ox) != int:
            raise TypeError("Expected int type for snowball_ox")

        if type(snowball_oy) != int:
            raise TypeError("Expected int type for snowball_oy")

        self.radius = radius
        self.move_velocity = move_velocity
        self.flash_velocity = flash_velocity
        self.sliding_friction = sliding_friction
        self.snowball_ox = snowball_ox
        self.snowball_oy = snowball_oy


class Snowball:
    def __init__(self, radius, fly_velocity):
        if type(radius) != int:
            raise TypeError("Expected int type for radius")

        if type(fly_velocity) != int:
            raise TypeError("Expected int type for fly_velocity")

        self.radius = radius
        self.fly_velocity = fly_velocity


class Specification:
    def __init__(self, world_mappings, island_mappings, penguin_mappings, snowball_mappings, insertions_mappings=None):
        self.world = World(world_mappings["max_x"], world_mappings["max_y"])
        self.island = Island(island_mappings["center_x"], island_mappings["center_y"], island_mappings["small_radius"],
                             island_mappings["big_radius"])
        self.penguin = Penguin(penguin_mappings["radius"], penguin_mappings["move_velocity"],
                               penguin_mappings["flash_velocity"], penguin_mappings["sliding_friction"],
                               penguin_mappings["snowball_ox"], penguin_mappings["snowball_oy"])
        self.snowball = Snowball(snowball_mappings["radius"], snowball_mappings["fly_velocity"])
        self.insertions = insertions_mappings or {}
