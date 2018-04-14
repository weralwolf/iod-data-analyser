from numpy import array


def smooth(x, window_len=11):
    result = []
    w2 = window_len // 2
    data_len = len(x)
    for i in range(data_len):
        db = min(i, w2)
        dt = min(data_len - 2 - i, w2 - 1)
        d = min(db, dt)
        sub_seq = x[i - d:i + d + 1]
        if i == data_len - 1:
            result.append(x[i])
        if len(sub_seq) == 0:
            result.append(0)
        else:
            result.append(sum(sub_seq) / (2 * d + 1))
    return array(result)
