from math import ceil, floor


def round(x):
    return ceil(x) if x - floor(x) > 0.5 else floor(x)
