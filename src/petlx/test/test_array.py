"""
Tests for the petlx.array module.

"""

import math
import numpy as np

from nose.tools import eq_
from petl.testutils import ieq

from petlx.array import toarray, fromarray, torecarray
from petlx.testutils import assertclose
import petl.fluent as etl


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
    eq_('apples', a['foo'][0])
    eq_('oranges', a['foo'][1])
    eq_('pears', a['foo'][2])
    eq_(1, a['bar'][0])
    eq_(3, a['bar'][1])
    eq_(7, a['bar'][2])
    assertclose(2.5, a['baz'][0])
    assertclose(4.4, a['baz'][1])
    assertclose(.1, a['baz'][2])


def test_torecarray():
    
    t = [('foo', 'bar', 'baz'),
         ('apples', 1, 2.5),
         ('oranges', 3, 4.4),
         ('pears', 7, .1)]
    
    a = torecarray(t)
    assert isinstance(a, np.ndarray)
    assert isinstance(a.foo, np.ndarray)
    assert isinstance(a.bar, np.ndarray)
    assert isinstance(a.baz, np.ndarray)
    eq_('apples', a.foo[0])
    eq_('oranges', a.foo[1])
    eq_('pears', a.foo[2])
    eq_(1, a.bar[0])
    eq_(3, a.bar[1])
    eq_(7, a.bar[2])
    assertclose(2.5, a.baz[0])
    assertclose(4.4, a.baz[1])
    assertclose(.1, a.baz[2])


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
    eq_('appl', a['foo'][0])
    eq_('oran', a['foo'][1])
    eq_('pear', a['foo'][2])
    eq_(1, a['bar'][0])
    eq_(3, a['bar'][1])
    eq_(7, a['bar'][2])
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
    eq_('appl', a['foo'][0])
    eq_('oran', a['foo'][1])
    eq_('pear', a['foo'][2])
    eq_(1, a['bar'][0])
    eq_(3, a['bar'][1])
    eq_(7, a['bar'][2])
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
    eq_('appl', a['A'][0])
    eq_('oran', a['A'][1])
    eq_('pear', a['A'][2])
    eq_(1, a['B'][0])
    eq_(3, a['B'][1])
    eq_(7, a['B'][2])
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
    eq_('apples', a['foo'][0])
    eq_('oranges', a['foo'][1])
    eq_('pears', a['foo'][2])
    eq_(1, a['bar'][0])
    eq_(3, a['bar'][1])
    eq_(7, a['bar'][2])
    assert math.fabs(2.5 - a['baz'][0]) < 0.001
    assert math.fabs(4.4 - a['baz'][1]) < 0.001
    assert math.fabs(.1 - a['baz'][2]) < 0.001
    
    
def test_fromarray():
    t = [('foo', 'bar', 'baz'),
         ('apples', 1, 2.5),
         ('oranges', 3, 4.4),
         ('pears', 7, .1)]
    a = toarray(t)
    u = fromarray(a)
    ieq(t, u)
    

def test_integration():
    t = etl.wrap([('foo', 'bar', 'baz'),
                  ('apples', 1, 2.5),
                  ('oranges', 3, 4.4),
                  ('pears', 7, .1)])
    a = t.toarray()
    u = etl.fromarray(a).convert('bar', int)
    ieq(t, u)


def test_valuesarray_no_dtype():

    t = [('foo', 'bar', 'baz'),
         ('apples', 1, 2.5),
         ('oranges', 3, 4.4),
         ('pears', 7, .1)]

    expect = np.array([1, 3, 7])
    actual = etl.wrap(t).values('bar').array()
    eq_(expect.dtype, actual.dtype)
    assert np.all(expect == actual)


def test_valuesarray_explicit_dtype():

    t = [('foo', 'bar', 'baz'),
         ('apples', 1, 2.5),
         ('oranges', 3, 4.4),
         ('pears', 7, .1)]

    expect = np.array([1, 3, 7], dtype='i2')
    actual = etl.wrap(t).values('bar').array(dtype='i2')
    eq_(expect.dtype, actual.dtype)
    assert np.all(expect == actual)
