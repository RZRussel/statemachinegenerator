import unittest
from physics import *


class TestPhysics(unittest.TestCase):
    def test_radial_moves(self):
        positions = set(radial_moves(1))
        assert len(positions) == 8
        assert (1, 1) in positions
        assert (0, 1) in positions
        assert (1, 0) in positions

    def test_rotate_position(self):
        positions = set(rotate_position((0, 1)))
        assert len(positions) == 8
        assert (1, 1) in positions
        assert (0, 1) in positions
        assert (1, 0) in positions

    def test_rotate_positions_vs_radial_moves(self):
        moves = set(radial_moves(5))
        rotations = set(rotate_position((0, 5)))

        assert moves == rotations
