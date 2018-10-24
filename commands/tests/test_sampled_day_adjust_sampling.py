from commands.artifacts.sampled_day import adjust_sampling

from numpy import all, array


def test_adjust_sampling_empty() -> None:
    end_of_sequence, sequence_filter = adjust_sampling([], 1)
    assert end_of_sequence == -1
    assert all(sequence_filter == array([]))


def test_adjust_sampling_ones() -> None:
    end_of_sequence, sequence_filter = adjust_sampling([1, 1, 1, 1, 1, 1, 1], 1)
    assert end_of_sequence == 6
    assert all(sequence_filter == array([0, 1, 2, 3, 4, 5, 6, 7]))


def test_adjust_sampling_twos() -> None:
    # osequence = [0, 1, 2, 4, 5, 6, 8, 9]
    # gsequence = [0,    2, 4,    6, 8   ]
    end_of_sequence, sequence_filter = adjust_sampling([1, 1, 2, 1, 1, 2, 1], 2)
    assert end_of_sequence == 6
    assert all(sequence_filter == array([0, 2, 3, 5, 6]))
