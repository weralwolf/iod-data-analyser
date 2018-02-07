import math

from ionospheredata.calc.per_element_map import pmap


def sin(arg):
    return pmap(math.sin, arg)

def cos(arg):
    return pmap(math.cos, arg)

def exp(arg):
    return pmap(math.exp, arg)

def fabs(arg):
    return pmap(math.fabs, arg)
