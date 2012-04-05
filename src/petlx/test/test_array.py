"""
Tests for the petlx.array module.

"""

import math
import numpy as np

from petl.testutils import assertequal

from petlx.array import toarray
from petlx.testutils import assertclose


def test_toarray_nodtype():
    
    t = [('foo', 'bar', 'baz'),
         ('apples', 1, 2.5),
         ('oranges', 3, 4.4),
         ('pears', 7, .1)]
    
    a = toarray(t)
    assert isinstance(a, np.ndarray)
    assert isinstance(a['foo'], np.ndarray)
    assert isinstance(a['bar'], np.ndarray)
    assert isinstance(a['baz'], np.ndarray)
    assertequal('apples', a['foo'][0])
    assertequal('oranges', a['foo'][1])
    assertequal('pears', a['foo'][2])
    assertequal(1, a['bar'][0])
    assertequal(3, a['bar'][1])
    assertequal(7, a['bar'][2])
    assertclose(2.5, a['baz'][0])
    assertclose(4.4, a['baz'][1])
    assertclose(.1, a['baz'][2])


def test_toarray_stringdtype():
    
    t = [('foo', 'bar', 'baz'),
         ('apples', 1, 2.5),
         ('oranges', 3, 4.4),
         ('pears', 7, .1)]
    
    a = toarray(t, dtype='a4, i2, f4')
    assert isinstance(a, np.ndarray)
    assert isinstance(a['foo'], np.ndarray)
    assert isinstance(a['bar'], np.ndarray)
    assert isinstance(a['baz'], np.ndarray)
    assertequal('appl', a['foo'][0])
    assertequal('oran', a['foo'][1])
    assertequal('pear', a['foo'][2])
    assertequal(1, a['bar'][0])
    assertequal(3, a['bar'][1])
    assertequal(7, a['bar'][2])
    assertclose(2.5, a['baz'][0])
    assertclose(4.4, a['baz'][1])
    assertclose(.1, a['baz'][2])


def test_toarray_dictdtype():
    
    t = [('foo', 'bar', 'baz'),
         ('apples', 1, 2.5),
         ('oranges', 3, 4.4),
         ('pears', 7, .1)]
    
    a = toarray(t, dtype={'foo': 'a4'}) # specify partial dtype
    assert isinstance(a, np.ndarray)
    assert isinstance(a['foo'], np.ndarray)
    assert isinstance(a['bar'], np.ndarray)
    assert isinstance(a['baz'], np.ndarray)
    assertequal('appl', a['foo'][0])
    assertequal('oran', a['foo'][1])
    assertequal('pear', a['foo'][2])
    assertequal(1, a['bar'][0])
    assertequal(3, a['bar'][1])
    assertequal(7, a['bar'][2])
    assertclose(2.5, a['baz'][0])
    assertclose(4.4, a['baz'][1])
    assertclose(.1, a['baz'][2])


def test_toarray_explicitdtype():
    
    t = [('foo', 'bar', 'baz'),
         ('apples', 1, 2.5),
         ('oranges', 3, 4.4),
         ('pears', 7, .1)]
    
    a = toarray(t, dtype=[('A', 'a4'), ('B', 'i2'), ('C', 'f4')])
    assert isinstance(a, np.ndarray)
    assert isinstance(a['A'], np.ndarray)
    assert isinstance(a['B'], np.ndarray)
    assert isinstance(a['C'], np.ndarray)
    assertequal('appl', a['A'][0])
    assertequal('oran', a['A'][1])
    assertequal('pear', a['A'][2])
    assertequal(1, a['B'][0])
    assertequal(3, a['B'][1])
    assertequal(7, a['B'][2])
    assertclose(2.5, a['C'][0])
    assertclose(4.4, a['C'][1])
    assertclose(.1, a['C'][2])


def test_toarray_lists():
    
    t = [['foo', 'bar', 'baz'],
         ['apples', 1, 2.5],
         ['oranges', 3, 4.4],
         ['pears', 7, .1]]
    
    a = toarray(t)
    assert isinstance(a, np.ndarray)
    assert isinstance(a['foo'], np.ndarray)
    assert isinstance(a['bar'], np.ndarray)
    assert isinstance(a['baz'], np.ndarray)
    assertequal('apples', a['foo'][0])
    assertequal('oranges', a['foo'][1])
    assertequal('pears', a['foo'][2])
    assertequal(1, a['bar'][0])
    assertequal(3, a['bar'][1])
    assertequal(7, a['bar'][2])
    assert math.fabs(2.5 - a['baz'][0]) < 0.001
    assert math.fabs(4.4 - a['baz'][1]) < 0.001
    assert math.fabs(.1 - a['baz'][2]) < 0.001
    
    
