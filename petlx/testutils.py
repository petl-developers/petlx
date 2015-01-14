"""
Unit test utilities.

"""


import math


def assertclose(e, a):
    assert math.fabs(e - a) < 0.00001, (e, a)
    
def assertis(e, a):
    assert e is a, (e, a)
    