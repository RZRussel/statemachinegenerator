

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

K_WORLD_MAX_X = "max_x"
K_WORLD_MAX_Y = "max_y"

K_ISLAND_CENTER_X = "center_x"
K_ISLAND_CENTER_Y = "center_y"
K_ISLAND_SMALL_RADIUS = "small_radius"
K_ISLAND_BIG_RADIUS = "big_radius"

K_PENGUIN_RADIUS = "radius"
K_PENGUIN_MOVE_VELOCITY = "move_velocity"
K_PENGUIN_FLASH_VELOCITY = "flash_velocity"
K_PENGUIN_SLIDING_FRICTION = "sliding_friction"
K_PENGUIN_SNOWBALL_OX = "snowball_ox"
K_PENGUIN_SNOWBALL_OY = "snowball_oy"

K_SNOWBALL_RADIUS = "radius"
K_SNOWBALL_FLY_VELOCITY = "fly_velocity"


class Specification:
    def __init__(self, world_mappings, island_mappings, penguin_mappings, snowball_mappings, insertions_mappings=None):
        self.world = World(world_mappings[K_WORLD_MAX_X], world_mappings[K_WORLD_MAX_Y])
        self.island = Island(island_mappings[K_ISLAND_CENTER_X], island_mappings[K_ISLAND_CENTER_Y],
                             island_mappings[K_ISLAND_SMALL_RADIUS], island_mappings[K_ISLAND_BIG_RADIUS])
        self.penguin = Penguin(penguin_mappings[K_PENGUIN_RADIUS], penguin_mappings[K_PENGUIN_MOVE_VELOCITY],
                               penguin_mappings[K_PENGUIN_FLASH_VELOCITY], penguin_mappings[K_PENGUIN_SLIDING_FRICTION],
                               penguin_mappings[K_PENGUIN_SNOWBALL_OX], penguin_mappings[K_PENGUIN_SNOWBALL_OY])
        self.snowball = Snowball(snowball_mappings[K_SNOWBALL_RADIUS], snowball_mappings[K_SNOWBALL_FLY_VELOCITY])
        self.insertions = insertions_mappings or {}

    @staticmethod
    def insertion_key(module_name, tag):
        """
        Static function to provide a way for building key to extract value from insertion mappings
        :param module_name: string name of the module tag belongs to
        :param tag: string tag representation
        :return: string key to access value in the insertions_mappings

        >>> Specification.insertion_key('Snowball', 'flew')
        'Snowball.flew'
        """
        return module_name + "." + tag

if __name__ == "__main__":
    import doctest
    doctest.testmod()
