from commands.artifacts.moving_average import moving_average_sequence as moving_average

from numpy import nan, array, isnan, around


def test_no_gaps_small_window() -> None:
    x = array([
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1
    ])
    avg_assert = array([
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 17.71428571, 18.14285714, 18.28571429,
        18.14285714, 17.71428571, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1
    ])
    avg_result = moving_average(x, window_len=7)
    assert all(around(avg_result, decimals=3) == around(avg_assert, decimals=3))


def test_no_gaps_large_window() -> None:
    x = array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
    avg_assert = array([
        1, 2, 3, 4, 5, 5.818181818, 6.076923077, 6, 5.705882353, 5.263157895,
        5.705882353, 6, 6.076923077, 5.818181818, 5, 4, 3, 2, 1
    ])
    avg_result = moving_average(x, window_len=25)
    assert all(around(avg_result, decimals=3) == around(avg_assert, decimals=3))


def test_gaps_small_window() -> None:
    x = array([
        1, 2, 3, 4, 5, nan, 7, 8, 9, 10, 11, nan, nan, 14, 15, 16, 17, 18, nan, 20,
        nan, 18, nan, 16, nan, 14, nan, 12, 11, 10, 9, 8, 7, 6, 5, 4, nan, 2, 1
    ])
    avg_assert = array([
        1, 2, 3, 3.666666667, 4.833333333, 6, 7.166666667, 8.333333333, 9, 9, 10.4, 11.8, 13.2, 14.6, 16, 16,
        16.66666667, 17.2, 17.8, 18.25, 18, 18, 17, 16, 15, 13.25, 12.6, 11.2, 10.66666667, 9.5, 9, 8, 7, 6.5,
        5.333333333, 4.166666667, 3, 1.5, 1
    ])
    avg_result = moving_average(x, window_len=7)
    assert all(around(avg_result, decimals=3) == around(avg_assert, decimals=3))


def test_gaps_large_window() -> None:
    x = array([
        1, 2, 3, nan, nan, nan, nan, 8, 9, 10, 9, 8, nan, 6, 5, nan, 3, 2, 1
    ])
    avg_assert = array([
        1, 2, 2, 2, 4.6, 6, 6.25, 6.1, 5.818181818, 5.153846154, 5.818181818, 6.1, 6.1, 5.888888889, 4.857142857, 3.4,
        2.75, 2, 1
    ])
    avg_result = moving_average(x, window_len=25)
    assert all(around(avg_result, decimals=3) == around(avg_assert, decimals=3))


def test_edge_gaps() -> None:
    x = array([nan, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, nan, nan, nan])
    avg_assert = array([
        nan, 2.5, 3.5, 4.5, 5.5, 6.3, 6.5, 6.357142857, 6.2, 6.2, 6.5, 7, 7.3, 7.25, 6.5, 5.5, 4.5, nan, nan
    ])
    avg_result = moving_average(x, window_len=25)

    # nan != nan... So we need to cheat
    avg_assert[isnan(avg_assert)] = -1
    avg_result[isnan(avg_result)] = -1
    assert all(around(avg_result, decimals=3) == around(avg_assert, decimals=3))
