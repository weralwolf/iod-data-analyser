from numpy import array
from numpy import matrix
from numpy import ndarray


def map_on_array(func, array_arg):
    return [func(array_arg[i]) for i in range(array_arg.shape[0])]

def map_on_matrix(func, matrix_arg):
    shape = matrix_arg.shape
    return matrix([[func(matrix_arg[i, j]) for j in range(shape[1])] for i in range(shape[0])])

def unwrapped_map_on_ndarray(func, ndarray_arg):
    shape = ndarray_arg.shape
    if len(shape) == 1:
        return map_on_array(func, ndarray_arg)
    return [unwrapped_map_on_ndarray(func, ndarray_arg[i]) for i in range(shape[0])]

def map_on_ndarray(func, ndarray_arg):
    if len(ndarray_arg.shape) == 1:
        return array(map_on_array(func, ndarray_arg))
    return array(unwrapped_map_on_ndarray(func, ndarray_arg))

def pmap(func, arg):
    if isinstance(arg, matrix):
        return map_on_matrix(func, arg)
    if isinstance(arg, ndarray):
        return map_on_ndarray(func, arg)
    return func(arg)
