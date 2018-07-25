from commands.artifacts.sampled_day import make_deltas

from numpy import all, array


def test_make_deltas_empty_array():
    deltas = make_deltas(array([]))
    assert all(deltas == array([]))


def test_make_deltas_single_point_array():
    deltas = make_deltas(array([1.]))
    assert all(deltas == array([]))


def test_make_deltas_even_sequence():
    deltas = make_deltas(array([1., 2., 3., 4., 5., 10.]))
    assert all(deltas == array([1, 1, 1, 1, 5]))


def test_make_deltas_fluctuated_sequence():
    deltas = make_deltas(array([1., 2.001, 2.999, 4.121, 5.982, 7.100]))
    assert all(deltas == array([1, 1, 1, 2, 1]))
