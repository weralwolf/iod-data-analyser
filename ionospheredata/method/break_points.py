from numpy import array


def break_points(ut: array, sampling: int):
    # Looking for break points and put in an array [UT(k-1) UT(k) BreakeSeconds]
    return array(list(filter(
        lambda point: point[2] != sampling,
        [
            [i_ut, i_ut + 1, ut[i_ut + 1] - ut[i_ut]]
            for i_ut in range(len(ut) - 1)
        ]
    )) + [[len(ut) - 1, len(ut), ut[-1] - ut[-2]]])
