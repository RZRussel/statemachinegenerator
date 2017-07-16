import unittest
from physics import *


class TestPhysics(unittest.TestCase):
    def test_radial_moves(self):
        positions = set(radial_moves(1))
        print(positions)
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

    def test_fading_velocities_list_property(self):
        velocities = fading_velocities_list(1.0, 1000)

        assert len(velocities) >= 2

        for i in range(0, len(velocities) - 1):
            assert velocities[i+1] >= velocities[i]

    def test_fading_velocity_sequence(self):
        velocities = fading_velocities_list(1.0, 10)

        assert velocities == [0, 1, 4, 10]

    def test_rotate_positions_vs_radial_moves(self):
        moves = set(radial_moves(5))
        rotations = set(rotate_position((0, 5)))

        assert moves == rotations

    def test_ellipsis_dead_points_generation(self):
        center = (20, 20)
        a = 10
        b = 15
        velocity = 5

        dead_points = reachable_points_from_ellipsis(center, a, b, velocity)

        assert len(dead_points) >= 4

        moves = set(radial_moves(5))
        for x, y in dead_points:
            assert not ellipsis_contains_position(center, a, b, (x, y))

            has_step = False
            for ox, oy in moves:
                if ellipsis_contains_position(center, a, b, (x + ox, y + oy)):
                    has_step = True
                    break
            assert has_step

    def test_collision_offsets(self):
        src_radius = 10
        src_velocity = 2
        dst_radius = 5
        dst_velocity = 1

        offsets = collision_offsets_for_circle_bodies(src_radius, src_velocity, dst_radius, dst_velocity)

        assert (src_radius + dst_radius, 0) in offsets
        assert (0, src_radius + dst_radius) in offsets
        assert (-(src_radius + dst_radius), 0) in offsets
        assert (0, -(src_radius + dst_radius)) in offsets

        for x, y in offsets:
            assert x*x + y*y <= (src_radius + dst_radius)*(src_radius + dst_radius)
