"""
Tests for the petlx.intervals module.

"""


from nose.tools import eq_


from petl.testutils import ieq
from petl.util import DuplicateKeyError, look
import petl.fluent as etl
from petlx.interval import intervallookup, intervallookupone, \
    facetintervallookup, facetintervallookupone, intervaljoin, \
    intervalleftjoin, intervaljoinvalues, intervalsubtract, collapsedintervals,\
    _Interval, intervalantijoin


def test_intervallookup():
    
    table = (('start', 'stop', 'value'),
             (1, 4, 'foo'),
             (3, 7, 'bar'),
             (4, 9, 'baz'))
    
    lkp = intervallookup(table, 'start', 'stop')
    
    actual = lkp.find(1, 2)
    expect = [(1, 4, 'foo')]
    ieq(expect, actual)
    
    actual = lkp.find(2, 4)
    expect = [(1, 4, 'foo'), (3, 7, 'bar')]
    ieq(expect, actual)
    
    actual = lkp.find(2, 5)
    expect = [(1, 4, 'foo'), (3, 7, 'bar'), (4, 9, 'baz')]
    ieq(expect, actual)
    
    actual = lkp.find(9, 14)
    expect = []
    ieq(expect, actual)
    
    actual = lkp.find(19, 140)
    expect = []
    ieq(expect, actual)
    
    actual = lkp.find(1)
    expect = []
    ieq(expect, actual)
    
    actual = lkp.find(2)
    expect = [(1, 4, 'foo')]
    ieq(expect, actual)
    
    actual = lkp.find(4)
    expect = [(3, 7, 'bar')]
    ieq(expect, actual)
    
    actual = lkp.find(5)
    expect = [(3, 7, 'bar'), (4, 9, 'baz')]
    ieq(expect, actual)
    
    
def test_intervallookup_2():
    
    table = (('start', 'stop', 'value'),
             (1, 4, 'foo'),
             (3, 7, 'bar'),
             (4, 9, 'baz'))
    
    lkp = intervallookup(table, 'start', 'stop', value='value', proximity=1)
    
    actual = lkp.find(1, 2)
    expect = ['foo']
    ieq(expect, actual)
    
    actual = lkp.find(2, 4)
    expect = ['foo', 'bar', 'baz']
    ieq(expect, actual)
    
    actual = lkp.find(2, 5)
    expect = ['foo', 'bar', 'baz']
    ieq(expect, actual)
    
    actual = lkp.find(9, 14)
    expect = ['baz']
    ieq(expect, actual)
    
    actual = lkp.find(19, 140)
    expect = []
    ieq(expect, actual)
    
    actual = lkp.find(1)
    expect = ['foo']
    print expect
    print actual
    ieq(expect, actual)
    
    actual = lkp.find(2)
    expect = ['foo']
    ieq(expect, actual)
    
    actual = lkp.find(4)
    expect = ['foo', 'bar', 'baz']
    ieq(expect, actual)
    
    actual = lkp.find(5)
    expect = ['bar', 'baz']
    ieq(expect, actual)


def test_intervallookupone():
    
    table = (('start', 'stop', 'value'),
             (1, 4, 'foo'),
             (3, 7, 'bar'),
             (4, 9, 'baz'))
    
    lkp = intervallookupone(table, 'start', 'stop', value='value')
    
    actual = lkp.find(1, 2)
    expect = 'foo'
    eq_(expect, actual)
    
    try:
        actual = lkp.find(2, 4)
    except DuplicateKeyError:
        pass
    else:
        assert False, 'expected error'
    
    try:
        actual = lkp.find(2, 5)
    except DuplicateKeyError:
        pass
    else:
        assert False, 'expected error'
    
    try:
        actual = lkp.find(4, 5)
    except DuplicateKeyError:
        pass
    else:
        assert False, 'expected error'
    
    try:
        actual = lkp.find(5, 7)
    except DuplicateKeyError:
        pass
    else:
        assert False, 'expected error'
    
    actual = lkp.find(8, 9)
    expect = 'baz'
    eq_(expect, actual)
    
    actual = lkp.find(9, 14)
    expect = None
    eq_(expect, actual)
    
    actual = lkp.find(19, 140)
    expect = None
    eq_(expect, actual)
    
    actual = lkp.find(1)
    expect = None
    eq_(expect, actual)
    
    actual = lkp.find(2)
    expect =  'foo'
    eq_(expect, actual)
    
    actual = lkp.find(4)
    expect = 'bar'
    eq_(expect, actual)
    
    try:
        actual = lkp.find(5)
    except DuplicateKeyError:
        pass
    else:
        assert False, 'expected error'
    
    actual = lkp.find(8)
    expect = 'baz'
    eq_(expect, actual)
    
    
def test_intervallookupone_2():
    
    table = (('start', 'stop', 'value'),
             (1, 4, 'foo'),
             (3, 7, 'bar'),
             (4, 9, 'baz'))
    
    lkp = intervallookupone(table, 'start', 'stop', value='value', strict=False)
    
    actual = lkp.find(1, 2)
    expect = 'foo'
    eq_(expect, actual)
    
    actual = lkp.find(2, 4)
    expect = 'foo'
    eq_(expect, actual)
    
    actual = lkp.find(2, 5)
    expect = 'foo'
    eq_(expect, actual)
    
    actual = lkp.find(4, 5)
    expect = 'bar'
    eq_(expect, actual)
    
    actual = lkp.find(5, 7)
    expect = 'bar'
    eq_(expect, actual)
    
    actual = lkp.find(8, 9)
    expect = 'baz'
    eq_(expect, actual)
    
    actual = lkp.find(9, 14)
    expect = None
    eq_(expect, actual)
    
    actual = lkp.find(19, 140)
    expect = None
    eq_(expect, actual)
    
    actual = lkp.find(1)
    expect = None
    eq_(expect, actual)
    
    actual = lkp.find(2)
    expect =  'foo'
    eq_(expect, actual)
    
    actual = lkp.find(4)
    expect = 'bar'
    ieq(expect, actual)
    
    actual = lkp.find(5)
    expect = 'bar'
    ieq(expect, actual)
    
    actual = lkp.find(8)
    expect = 'baz'
    ieq(expect, actual)
    
    
def test_facetintervallookup():
    
    table = (('type', 'start', 'stop', 'value'),
             ('apple', 1, 4, 'foo'),
             ('apple', 3, 7, 'bar'),
             ('orange', 4, 9, 'baz'))
    
    lkp = facetintervallookup(table, facet='type', start='start', stop='stop')

    actual = lkp['apple'].find(1, 2)
    expect = [('apple', 1, 4, 'foo')]
    ieq(expect, actual)
    
    actual = lkp['apple'].find(2, 4)
    expect = [('apple', 1, 4, 'foo'), ('apple', 3, 7, 'bar')]
    ieq(expect, actual)
    
    actual = lkp['apple'].find(2, 5)
    expect = [('apple', 1, 4, 'foo'), ('apple', 3, 7, 'bar')]
    ieq(expect, actual)
    
    actual = lkp['orange'].find(2, 5)
    expect = [('orange', 4, 9, 'baz')]
    ieq(expect, actual)
    
    actual = lkp['orange'].find(9, 14)
    expect = []
    ieq(expect, actual)
    
    actual = lkp['orange'].find(19, 140)
    expect = []
    ieq(expect, actual)
    
    actual = lkp['apple'].find(1)
    expect = []
    ieq(expect, actual)
    
    actual = lkp['apple'].find(2)
    expect = [('apple', 1, 4, 'foo')]
    ieq(expect, actual)
    
    actual = lkp['apple'].find(4)
    expect = [('apple', 3, 7, 'bar')]
    ieq(expect, actual)
    
    actual = lkp['apple'].find(5)
    expect = [('apple', 3, 7, 'bar')]
    ieq(expect, actual)
    
    actual = lkp['orange'].find(5)
    expect = [('orange', 4, 9, 'baz')]
    ieq(expect, actual)


def test_facetintervallookupone():
    
    table = (('type', 'start', 'stop', 'value'),
             ('apple', 1, 4, 'foo'),
             ('apple', 3, 7, 'bar'),
             ('orange', 4, 9, 'baz'))
    
    lkp = facetintervallookupone(table, facet='type', start='start', stop='stop', value='value')
    
    actual = lkp['apple'].find(1, 2)
    expect = 'foo'
    eq_(expect, actual)
    
    try:
        actual = lkp['apple'].find(2, 4)
    except DuplicateKeyError:
        pass
    else:
        assert False, 'expected error'
    
    try:
        actual = lkp['apple'].find(2, 5)
    except DuplicateKeyError:
        pass
    else:
        assert False, 'expected error'
    
    actual = lkp['apple'].find(4, 5)
    expect = 'bar'
    eq_(expect, actual)
    
    actual = lkp['orange'].find(4, 5)
    expect = 'baz'
    eq_(expect, actual)
    
    actual = lkp['apple'].find(5, 7)
    expect = 'bar'
    eq_(expect, actual)

    actual = lkp['orange'].find(5, 7)
    expect = 'baz'
    eq_(expect, actual)
    
    actual = lkp['apple'].find(8, 9)
    expect = None
    eq_(expect, actual)
    
    actual = lkp['orange'].find(8, 9)
    expect = 'baz'
    eq_(expect, actual)
    
    actual = lkp['orange'].find(9, 14)
    expect = None
    eq_(expect, actual)
    
    actual = lkp['orange'].find(19, 140)
    expect = None
    eq_(expect, actual)
    
    actual = lkp['apple'].find(1)
    expect = None
    eq_(expect, actual)
    
    actual = lkp['apple'].find(2)
    expect =  'foo'
    eq_(expect, actual)
    
    actual = lkp['apple'].find(4)
    expect = 'bar'
    eq_(expect, actual)
    
    actual = lkp['apple'].find(5)
    expect = 'bar'
    eq_(expect, actual)
    
    actual = lkp['orange'].find(5)
    expect = 'baz'
    eq_(expect, actual)
    
    actual = lkp['apple'].find(8)
    expect = None
    eq_(expect, actual)
    
    actual = lkp['orange'].find(8)
    expect = 'baz'
    eq_(expect, actual)
    
    
def test_facetintervallookup_compound():

    table = (('type', 'variety', 'start', 'stop', 'value'),
             ('apple', 'cox', 1, 4, 'foo'),
             ('apple', 'fuji', 3, 7, 'bar'),
             ('orange', 'mandarin', 4, 9, 'baz'))

    lkp = facetintervallookup(table, facet=('type', 'variety'), start='start',
                              stop='stop')

    actual = lkp['apple', 'cox'].find(1, 2)
    expect = [('apple', 'cox', 1, 4, 'foo')]
    ieq(expect, actual)

    actual = lkp['apple', 'cox'].find(2, 4)
    expect = [('apple', 'cox', 1, 4, 'foo')]
    ieq(expect, actual)


def test_intervaljoin():
    
    left = (('begin', 'end', 'quux'),
            (1, 2, 'a'),
            (2, 4, 'b'),
            (2, 5, 'c'),
            (9, 14, 'd'),
            (9, 140, 'e'),
            (1, 1, 'f'),
            (2, 2, 'g'),
            (4, 4, 'h'),
            (5, 5, 'i'),
            (1, 8, 'j'))

    right = (('start', 'stop', 'value'),
             (1, 4, 'foo'),
             (3, 7, 'bar'),
             (4, 9, 'baz'))

    actual = intervaljoin(left, right, 
                          lstart='begin', lstop='end',
                          rstart='start', rstop='stop')
    expect = (('begin', 'end', 'quux', 'start', 'stop', 'value'),
              (1, 2, 'a', 1, 4, 'foo'),
              (2, 4, 'b', 1, 4, 'foo'),
              (2, 4, 'b', 3, 7, 'bar'),
              (2, 5, 'c', 1, 4, 'foo'),
              (2, 5, 'c', 3, 7, 'bar'),
              (2, 5, 'c', 4, 9, 'baz'),
              (2, 2, 'g', 1, 4, 'foo'),
              (4, 4, 'h', 3, 7, 'bar'),
              (5, 5, 'i', 3, 7, 'bar'),
              (5, 5, 'i', 4, 9, 'baz'),
              (1, 8, 'j', 1, 4, 'foo'),
              (1, 8, 'j', 3, 7, 'bar'),
              (1, 8, 'j', 4, 9, 'baz'))
    ieq(expect, actual)
    ieq(expect, actual)
    
    
def test_intervaljoin_proximity():
    
    left = (('begin', 'end', 'quux'),
            (1, 2, 'a'),
            (2, 4, 'b'),
            (2, 5, 'c'),
            (9, 14, 'd'),
            (9, 140, 'e'),
            (1, 1, 'f'),
            (2, 2, 'g'),
            (4, 4, 'h'),
            (5, 5, 'i'),
            (1, 8, 'j'))

    right = (('start', 'stop', 'value'),
             (1, 4, 'foo'),
             (3, 7, 'bar'),
             (4, 9, 'baz'))

    actual = intervaljoin(left, right, 
                          lstart='begin', lstop='end',
                          rstart='start', rstop='stop',
                          proximity=1)
    expect = (('begin', 'end', 'quux', 'start', 'stop', 'value'),
              (1, 2, 'a', 1, 4, 'foo'),
              (2, 4, 'b', 1, 4, 'foo'),
              (2, 4, 'b', 3, 7, 'bar'),
              (2, 4, 'b', 4, 9, 'baz'),
              (2, 5, 'c', 1, 4, 'foo'),
              (2, 5, 'c', 3, 7, 'bar'),
              (2, 5, 'c', 4, 9, 'baz'),
              (9, 14, 'd', 4, 9, 'baz'),
              (9, 140, 'e', 4, 9, 'baz'),
              (1, 1, 'f', 1, 4, 'foo'),
              (2, 2, 'g', 1, 4, 'foo'),
              (4, 4, 'h', 1, 4, 'foo'),
              (4, 4, 'h', 3, 7, 'bar'),
              (4, 4, 'h', 4, 9, 'baz'),
              (5, 5, 'i', 3, 7, 'bar'),
              (5, 5, 'i', 4, 9, 'baz'),
              (1, 8, 'j', 1, 4, 'foo'),
              (1, 8, 'j', 3, 7, 'bar'),
              (1, 8, 'j', 4, 9, 'baz'))
    ieq(expect, actual)
    ieq(expect, actual)
    
    
def test_intervaljoin_prefixes():

    left = (('begin', 'end', 'quux'),
            (1, 2, 'a'),
            (2, 4, 'b'),
            (2, 5, 'c'),
            (9, 14, 'd'),
            (9, 140, 'e'),
            (1, 1, 'f'),
            (2, 2, 'g'),
            (4, 4, 'h'),
            (5, 5, 'i'),
            (1, 8, 'j'))

    right = (('start', 'stop', 'value'),
             (1, 4, 'foo'),
             (3, 7, 'bar'),
             (4, 9, 'baz'))

    actual = intervaljoin(left, right,
                          lstart='begin', lstop='end',
                          rstart='start', rstop='stop',
                          lprefix='l_', rprefix='r_')
    expect = (('l_begin', 'l_end', 'l_quux', 'r_start', 'r_stop', 'r_value'),
              (1, 2, 'a', 1, 4, 'foo'),
              (2, 4, 'b', 1, 4, 'foo'),
              (2, 4, 'b', 3, 7, 'bar'),
              (2, 5, 'c', 1, 4, 'foo'),
              (2, 5, 'c', 3, 7, 'bar'),
              (2, 5, 'c', 4, 9, 'baz'),
              (2, 2, 'g', 1, 4, 'foo'),
              (4, 4, 'h', 3, 7, 'bar'),
              (5, 5, 'i', 3, 7, 'bar'),
              (5, 5, 'i', 4, 9, 'baz'),
              (1, 8, 'j', 1, 4, 'foo'),
              (1, 8, 'j', 3, 7, 'bar'),
              (1, 8, 'j', 4, 9, 'baz'))
    ieq(expect, actual)
    ieq(expect, actual)


def test_intervalleftjoin():
    
    left = (('begin', 'end', 'quux'),
            (1, 2, 'a'),
            (2, 4, 'b'),
            (2, 5, 'c'),
            (9, 14, 'd'),
            (9, 140, 'e'),
            (1, 1, 'f'),
            (2, 2, 'g'),
            (4, 4, 'h'),
            (5, 5, 'i'),
            (1, 8, 'j'))

    right = (('start', 'stop', 'value'),
             (1, 4, 'foo'),
             (3, 7, 'bar'),
             (4, 9, 'baz'))

    actual = intervalleftjoin(left, right, 
                              lstart='begin', lstop='end',
                              rstart='start', rstop='stop')
    expect = (('begin', 'end', 'quux', 'start', 'stop', 'value'),
              (1, 2, 'a', 1, 4, 'foo'),
              (2, 4, 'b', 1, 4, 'foo'),
              (2, 4, 'b', 3, 7, 'bar'),
              (2, 5, 'c', 1, 4, 'foo'),
              (2, 5, 'c', 3, 7, 'bar'),
              (2, 5, 'c', 4, 9, 'baz'),
              (9, 14, 'd', None, None, None),
              (9, 140, 'e', None, None, None),
              (1, 1, 'f', None, None, None),
              (2, 2, 'g', 1, 4, 'foo'),
              (4, 4, 'h', 3, 7, 'bar'),
              (5, 5, 'i', 3, 7, 'bar'),
              (5, 5, 'i', 4, 9, 'baz'),
              (1, 8, 'j', 1, 4, 'foo'),
              (1, 8, 'j', 3, 7, 'bar'),
              (1, 8, 'j', 4, 9, 'baz'))
    ieq(expect, actual)
    ieq(expect, actual)
    

def test_intervaljoin_faceted():    

    left = (('fruit', 'begin', 'end'),
            ('apple', 1, 2),
            ('apple', 2, 4),
            ('apple', 2, 5),
            ('orange', 2, 5),
            ('orange', 9, 14),
            ('orange', 19, 140),
            ('apple', 1, 1),
            ('apple', 2, 2),
            ('apple', 4, 4),
            ('apple', 5, 5),
            ('orange', 5, 5))

    right = (('type', 'start', 'stop', 'value'),
             ('apple', 1, 4, 'foo'),
             ('apple', 3, 7, 'bar'),
             ('orange', 4, 9, 'baz'))
    
    expect = (('fruit', 'begin', 'end', 'type', 'start', 'stop', 'value'),
              ('apple', 1, 2, 'apple', 1, 4, 'foo'),
              ('apple', 2, 4, 'apple', 1, 4, 'foo'),
              ('apple', 2, 4, 'apple', 3, 7, 'bar'),
              ('apple', 2, 5, 'apple', 1, 4, 'foo'),
              ('apple', 2, 5, 'apple', 3, 7, 'bar'),
              ('orange', 2, 5, 'orange', 4, 9, 'baz'),
              ('apple', 2, 2, 'apple', 1, 4, 'foo'),
              ('apple', 4, 4, 'apple', 3, 7, 'bar'),
              ('apple', 5, 5, 'apple', 3, 7, 'bar'),
              ('orange', 5, 5, 'orange', 4, 9, 'baz'))

    actual = intervaljoin(left, right, lstart='begin', lstop='end', 
                          rstart='start', rstop='stop', lfacet='fruit',
                          rfacet='type')

    ieq(expect, actual)
    ieq(expect, actual)

               
def test_intervalleftjoin_faceted():

    left = (('fruit', 'begin', 'end'),
            ('apple', 1, 2),
            ('apple', 2, 4),
            ('apple', 2, 5),
            ('orange', 2, 5),
            ('orange', 9, 14),
            ('orange', 19, 140),
            ('apple', 1, 1),
            ('apple', 2, 2),
            ('apple', 4, 4),
            ('apple', 5, 5),
            ('orange', 5, 5))

    right = (('type', 'start', 'stop', 'value'),
             ('apple', 1, 4, 'foo'),
             ('apple', 3, 7, 'bar'),
             ('orange', 4, 9, 'baz'))
    
    expect = (('fruit', 'begin', 'end', 'type', 'start', 'stop', 'value'),
              ('apple', 1, 2, 'apple', 1, 4, 'foo'),
              ('apple', 2, 4, 'apple', 1, 4, 'foo'),
              ('apple', 2, 4, 'apple', 3, 7, 'bar'),
              ('apple', 2, 5, 'apple', 1, 4, 'foo'),
              ('apple', 2, 5, 'apple', 3, 7, 'bar'),
              ('orange', 2, 5, 'orange', 4, 9, 'baz'),
              ('orange', 9, 14, None, None, None, None),
              ('orange', 19, 140, None, None, None, None),
              ('apple', 1, 1, None, None, None, None),
              ('apple', 2, 2, 'apple', 1, 4, 'foo'),
              ('apple', 4, 4, 'apple', 3, 7, 'bar'),
              ('apple', 5, 5, 'apple', 3, 7, 'bar'),
              ('orange', 5, 5, 'orange', 4, 9, 'baz'))

    actual = intervalleftjoin(left, right, lstart='begin', lstop='end', 
                              rstart='start', rstop='stop', lfacet='fruit',
                              rfacet='type')

    ieq(expect, actual)
    ieq(expect, actual)
    
    
def test_intervalleftjoin_faceted_rkeymissing():    

    left = (('fruit', 'begin', 'end'),
            ('apple', 1, 2),
            ('orange', 5, 5))

    right = (('type', 'start', 'stop', 'value'),
             ('apple', 1, 4, 'foo'))
        
    expect = (('fruit', 'begin', 'end', 'type', 'start', 'stop', 'value'),
              ('apple', 1, 2, 'apple', 1, 4, 'foo'),
              ('orange', 5, 5, None, None, None, None))

    actual = intervalleftjoin(left, right, lstart='begin', lstop='end', 
                              rstart='start', rstop='stop', lfacet='fruit',
                              rfacet='type')

    ieq(expect, actual)
    ieq(expect, actual)


def test_intervaljoins_faceted_compound():

    left = (('fruit', 'sort', 'begin', 'end'),
            ('apple', 'cox', 1, 2),
            ('apple', 'fuji', 2, 4))
    right = (('type', 'variety', 'start', 'stop', 'value'),
             ('apple', 'cox', 1, 4, 'foo'),
             ('apple', 'fuji', 3, 7, 'bar'),
             ('orange', 'mandarin', 4, 9, 'baz'))

    expect = (('fruit', 'sort', 'begin', 'end', 'type', 'variety', 'start',
               'stop', 'value'),
              ('apple', 'cox', 1, 2, 'apple', 'cox', 1, 4, 'foo'),
              ('apple', 'fuji', 2, 4, 'apple', 'fuji', 3, 7, 'bar'))

    actual = intervaljoin(left, right, lstart='begin', lstop='end',
                          rstart='start', rstop='stop',
                          lfacet=('fruit', 'sort'),
                          rfacet=('type', 'variety'))
    ieq(expect, actual)
    ieq(expect, actual)

    actual = intervalleftjoin(left, right, lstart='begin', lstop='end',
                              rstart='start', rstop='stop',
                              lfacet=('fruit', 'sort'),
                              rfacet=('type', 'variety'))
    ieq(expect, actual)
    ieq(expect, actual)



def test_intervalleftjoin_prefixes():

    left = (('begin', 'end', 'quux'),
            (1, 2, 'a'),
            (2, 4, 'b'),
            (2, 5, 'c'),
            (9, 14, 'd'),
            (9, 140, 'e'),
            (1, 1, 'f'),
            (2, 2, 'g'),
            (4, 4, 'h'),
            (5, 5, 'i'),
            (1, 8, 'j'))

    right = (('start', 'stop', 'value'),
             (1, 4, 'foo'),
             (3, 7, 'bar'),
             (4, 9, 'baz'))

    actual = intervalleftjoin(left, right,
                              lstart='begin', lstop='end',
                              rstart='start', rstop='stop',
                              lprefix='l_', rprefix='r_')
    expect = (('l_begin', 'l_end', 'l_quux', 'r_start', 'r_stop', 'r_value'),
              (1, 2, 'a', 1, 4, 'foo'),
              (2, 4, 'b', 1, 4, 'foo'),
              (2, 4, 'b', 3, 7, 'bar'),
              (2, 5, 'c', 1, 4, 'foo'),
              (2, 5, 'c', 3, 7, 'bar'),
              (2, 5, 'c', 4, 9, 'baz'),
              (9, 14, 'd', None, None, None),
              (9, 140, 'e', None, None, None),
              (1, 1, 'f', None, None, None),
              (2, 2, 'g', 1, 4, 'foo'),
              (4, 4, 'h', 3, 7, 'bar'),
              (5, 5, 'i', 3, 7, 'bar'),
              (5, 5, 'i', 4, 9, 'baz'),
              (1, 8, 'j', 1, 4, 'foo'),
              (1, 8, 'j', 3, 7, 'bar'),
              (1, 8, 'j', 4, 9, 'baz'))
    ieq(expect, actual)
    ieq(expect, actual)


def test_intervalantijoin():

    left = (('begin', 'end', 'quux'),
            (1, 2, 'a'),
            (2, 4, 'b'),
            (2, 5, 'c'),
            (9, 14, 'd'),
            (9, 140, 'e'),
            (1, 1, 'f'),
            (2, 2, 'g'),
            (4, 4, 'h'),
            (5, 5, 'i'),
            (1, 8, 'j'))

    right = (('start', 'stop', 'value'),
             (1, 4, 'foo'),
             (3, 7, 'bar'),
             (4, 9, 'baz'))

    actual = intervalantijoin(left, right,
                              lstart='begin', lstop='end',
                              rstart='start', rstop='stop')
    expect = (('begin', 'end', 'quux'),
              (9, 14, 'd'),
              (9, 140, 'e'),
              (1, 1, 'f'))
    ieq(expect, actual)
    ieq(expect, actual)


def test_intervalantijoin_faceted():

    left = (('fruit', 'begin', 'end'),
            ('apple', 1, 2),
            ('apple', 2, 4),
            ('apple', 2, 5),
            ('orange', 2, 5),
            ('orange', 9, 14),
            ('orange', 19, 140),
            ('apple', 1, 1),
            ('apple', 2, 2),
            ('apple', 4, 4),
            ('apple', 5, 5),
            ('orange', 5, 5))

    right = (('type', 'start', 'stop', 'value'),
             ('apple', 1, 4, 'foo'),
             ('apple', 3, 7, 'bar'),
             ('orange', 4, 9, 'baz'))

    expect = (('fruit', 'begin', 'end'),
              ('orange', 9, 14),
              ('orange', 19, 140),
              ('apple', 1, 1))

    actual = intervalantijoin(left, right, lstart='begin', lstop='end',
                              rstart='start', rstop='stop', lfacet='fruit',
                              rfacet='type')

    ieq(expect, actual)
    ieq(expect, actual)


def test_intervaljoinvalues_faceted():

    left = (('fruit', 'begin', 'end'),
            ('apple', 1, 2),
            ('apple', 2, 4),
            ('apple', 2, 5),
            ('orange', 2, 5),
            ('orange', 9, 14),
            ('orange', 19, 140),
            ('apple', 1, 1),
            ('apple', 2, 2),
            ('apple', 4, 4),
            ('apple', 5, 5),
            ('orange', 5, 5))

    right = (('type', 'start', 'stop', 'value'),
             ('apple', 1, 4, 'foo'),
             ('apple', 3, 7, 'bar'),
             ('orange', 4, 9, 'baz'))
    
    expect = (('fruit', 'begin', 'end', 'value'),
              ('apple', 1, 2, ['foo']),
              ('apple', 2, 4, ['foo', 'bar']),
              ('apple', 2, 5, ['foo', 'bar']),
              ('orange', 2, 5, ['baz']),
              ('orange', 9, 14, []),
              ('orange', 19, 140, []),
              ('apple', 1, 1, []),
              ('apple', 2, 2, ['foo']),
              ('apple', 4, 4, ['bar']),
              ('apple', 5, 5, ['bar']),
              ('orange', 5, 5, ['baz']))

    actual = intervaljoinvalues(left, right, lstart='begin', lstop='end', 
                                rstart='start', rstop='stop', lfacet='fruit',
                                rfacet='type', value='value')

    ieq(expect, actual)
    ieq(expect, actual)
    
    
def test_subtract_1():
    
    left = (('begin', 'end', 'label'),
            (1, 6, 'apple'),
            (3, 6, 'orange'),
            (5, 9, 'banana'))
    
    right = (('start', 'stop', 'foo'),
             (3, 4, True))
    
    expect = (('begin', 'end', 'label'),
              (1, 3, 'apple'),
              (4, 6, 'apple'),
              (4, 6, 'orange'),
              (5, 9, 'banana'))
    
    actual = intervalsubtract(left, right, 
                              lstart='begin', lstop='end', 
                              rstart='start', rstop='stop')
    print look(actual)

    ieq(expect, actual)
    ieq(expect, actual)
    
        
def test_subtract_2():
    
    left = (('begin', 'end', 'label'),
            (1, 6, 'apple'),
            (3, 6, 'orange'),
            (5, 9, 'banana'))
    
    right = (('start', 'stop', 'foo'),
             (3, 4, True),
             (5, 6, True))
    
    expect = (('begin', 'end', 'label'),
              (1, 3, 'apple'),
              (4, 5, 'apple'),
              (4, 5, 'orange'),
              (6, 9, 'banana'))
    
    actual = intervalsubtract(left, right, 
                              lstart='begin', lstop='end', 
                              rstart='start', rstop='stop')
    print look(actual)

    ieq(expect, actual)
    ieq(expect, actual)
    
        
def test_subtract_faceted():
    
    left = (('region', 'begin', 'end', 'label'),
            ('north', 1, 6, 'apple'),
            ('south', 3, 6, 'orange'),
            ('west', 5, 9, 'banana'))
    
    right = (('place', 'start', 'stop', 'foo'),
             ('south', 3, 4, True),
             ('north', 5, 6, True))
    
    expect = (('region', 'begin', 'end', 'label'),
              ('north', 1, 5, 'apple'),
              ('south', 4, 6, 'orange'),
              ('west', 5, 9, 'banana'))
    
    actual = intervalsubtract(left, right,
                              lfacet='region', rfacet='place', 
                              lstart='begin', lstop='end', 
                              rstart='start', rstop='stop')
    print look(actual)

    ieq(expect, actual)
    ieq(expect, actual)
    

def test_collapse():
    
    # no facet key
    tbl = (('begin', 'end', 'label'),
            (1, 6, 'apple'),
            (3, 6, 'orange'),
            (5, 9, 'banana'),
            (12, 14, 'banana'),
            (13, 17, 'kiwi'))
    expect = [_Interval(1, 9), _Interval(12, 17)]
    actual = collapsedintervals(tbl, start='begin', stop='end')
    ieq(expect, actual)    
            
    # faceted 
    tbl = (('region', 'begin', 'end', 'label'),
            ('north', 1, 6, 'apple'),
            ('north', 3, 6, 'orange'),
            ('north', 5, 9, 'banana'),
            ('south', 12, 14, 'banana'),
            ('south', 13, 17, 'kiwi'))
    expect = [('north', 1, 9), ('south', 12, 17)]
    actual = collapsedintervals(tbl, start='begin', stop='end', facet='region')
    ieq(expect, actual)    
            
    
def test_integration():
    
    left = etl.wrap((('begin', 'end', 'quux'),
                     (1, 2, 'a'),
                     (2, 4, 'b'),
                     (2, 5, 'c'),
                     (9, 14, 'd'),
                     (9, 140, 'e'),
                     (1, 1, 'f'),
                     (2, 2, 'g'),
                     (4, 4, 'h'),
                     (5, 5, 'i'),
                     (1, 8, 'j')))

    right = etl.wrap((('start', 'stop', 'value'),
                      (1, 4, 'foo'),
                      (3, 7, 'bar'),
                      (4, 9, 'baz')))

    actual = left.intervaljoin(right, 
                               lstart='begin', lstop='end',
                               rstart='start', rstop='stop')
    expect = (('begin', 'end', 'quux', 'start', 'stop', 'value'),
              (1, 2, 'a', 1, 4, 'foo'),
              (2, 4, 'b', 1, 4, 'foo'),
              (2, 4, 'b', 3, 7, 'bar'),
              (2, 5, 'c', 1, 4, 'foo'),
              (2, 5, 'c', 3, 7, 'bar'),
              (2, 5, 'c', 4, 9, 'baz'),
              (2, 2, 'g', 1, 4, 'foo'),
              (4, 4, 'h', 3, 7, 'bar'),
              (5, 5, 'i', 3, 7, 'bar'),
              (5, 5, 'i', 4, 9, 'baz'),
              (1, 8, 'j', 1, 4, 'foo'),
              (1, 8, 'j', 3, 7, 'bar'),
              (1, 8, 'j', 4, 9, 'baz'))
    ieq(expect, actual)
    ieq(expect, actual)
