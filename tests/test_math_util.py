"""Sanity tests for math helpers."""
from src.utils.math_util import vec3_distance, vec3_sub


def test_distance_zero():
    assert vec3_distance((1.0, 2.0, 3.0), (1.0, 2.0, 3.0)) == 0.0


def test_distance_axis():
    assert vec3_distance((0.0, 0.0, 0.0), (3.0, 4.0, 0.0)) == 5.0


def test_sub():
    assert vec3_sub((5.0, 5.0, 5.0), (1.0, 2.0, 3.0)) == (4.0, 3.0, 2.0)