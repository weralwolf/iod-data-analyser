from numpy import arange

# """Generates a list of values from `start` to `end` with length of `number`.

# Args:
# 	start (int): start of the linear space
# 	end (int): other end of linear space
# 	number (int): number of points

# Returns:
# 	array: linear space array of points
# """
def linspace(start: int, end: int, number: int):
    return arange(start, end, (end - start) / number)
