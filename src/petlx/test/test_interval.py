"""
Tests for the petlx.intervals module.

"""

from petl.testutils import iassertequal, assertequal
from petl.util import DuplicateKeyError

from petlx.interval import intervallookup, intervallookupone, facetintervallookup, \
                        facetintervallookupone, intervaljoin, intervalleftjoin


def test_intervallookup():
    
    table = (('start', 'stop', 'value'),
             (1, 4, 'foo'),
             (3, 7, 'bar'),
             (4, 9, 'baz'))
    
    lkp = intervallookup(table, 'start', 'stop')
    
    actual = lkp[1:2]
    expect = [(1, 4, 'foo')]
    iassertequal(expect, actual)
    
    actual = lkp[2:4]
    expect = [(1, 4, 'foo'), (3, 7, 'bar')]
    iassertequal(expect, actual)
    
    actual = lkp[2:5]
    expect = [(1, 4, 'foo'), (3, 7, 'bar'), (4, 9, 'baz')]
    iassertequal(expect, actual)
    
    actual = lkp[9:14]
    expect = []
    iassertequal(expect, actual)
    
    actual = lkp[19:140]
    expect = []
    iassertequal(expect, actual)
    
    actual = lkp[1]
    expect = []
    iassertequal(expect, actual)
    
    actual = lkp[2]
    expect = [(1, 4, 'foo')]
    iassertequal(expect, actual)
    
    actual = lkp[4]
    expect = [(3, 7, 'bar')]
    iassertequal(expect, actual)
    
    actual = lkp[5]
    expect = [(3, 7, 'bar'), (4, 9, 'baz')]
    iassertequal(expect, actual)
    
    
def test_intervallookup_2():
    
    table = (('start', 'stop', 'value'),
             (1, 4, 'foo'),
             (3, 7, 'bar'),
             (4, 9, 'baz'))
    
    lkp = intervallookup(table, 'start', 'stop', valuespec='value', proximity=1)
    
    actual = lkp[1:2]
    expect = ['foo']
    iassertequal(expect, actual)
    
    actual = lkp[2:4]
    expect = ['foo', 'bar', 'baz']
    iassertequal(expect, actual)
    
    actual = lkp[2:5]
    expect = ['foo', 'bar', 'baz']
    iassertequal(expect, actual)
    
    actual = lkp[9:14]
    expect = ['baz']
    iassertequal(expect, actual)
    
    actual = lkp[19:140]
    expect = []
    iassertequal(expect, actual)
    
    actual = lkp[1]
    expect = ['foo']
    iassertequal(expect, actual)
    
    actual = lkp[2]
    expect = ['foo']
    iassertequal(expect, actual)
    
    actual = lkp[4]
    expect = ['foo', 'bar', 'baz']
    iassertequal(expect, actual)
    
    actual = lkp[5]
    expect = ['bar', 'baz']
    iassertequal(expect, actual)


def test_intervallookupone():
    
    table = (('start', 'stop', 'value'),
             (1, 4, 'foo'),
             (3, 7, 'bar'),
             (4, 9, 'baz'))
    
    lkp = intervallookupone(table, 'start', 'stop', valuespec='value')
    
    actual = lkp[1:2]
    expect = 'foo'
    assertequal(expect, actual)
    
    try:
        actual = lkp[2:4]
    except DuplicateKeyError:
        pass
    else:
        assert False, 'expected error'
    
    try:
        actual = lkp[2:5]
    except DuplicateKeyError:
        pass
    else:
        assert False, 'expected error'
    
    try:
        actual = lkp[4:5]
    except DuplicateKeyError:
        pass
    else:
        assert False, 'expected error'
    
    try:
        actual = lkp[5:7]
    except DuplicateKeyError:
        pass
    else:
        assert False, 'expected error'
    
    actual = lkp[8:9]
    expect = 'baz'
    assertequal(expect, actual)
    
    actual = lkp[9:14]
    expect = None
    assertequal(expect, actual)
    
    actual = lkp[19:140]
    expect = None
    assertequal(expect, actual)
    
    actual = lkp[1]
    expect = None
    assertequal(expect, actual)
    
    actual = lkp[2]
    expect =  'foo'
    assertequal(expect, actual)
    
    actual = lkp[4]
    expect = 'bar'
    assertequal(expect, actual)
    
    try:
        actual = lkp[5]
    except DuplicateKeyError:
        pass
    else:
        assert False, 'expected error'
    
    actual = lkp[8]
    expect = 'baz'
    assertequal(expect, actual)
    
    
def test_intervallookupone_2():
    
    table = (('start', 'stop', 'value'),
             (1, 4, 'foo'),
             (3, 7, 'bar'),
             (4, 9, 'baz'))
    
    lkp = intervallookupone(table, 'start', 'stop', valuespec='value', strict=False)
    
    actual = lkp[1:2]
    expect = 'foo'
    assertequal(expect, actual)
    
    actual = lkp[2:4]
    expect = 'foo'
    assertequal(expect, actual)
    
    actual = lkp[2:5]
    expect = 'foo'
    assertequal(expect, actual)
    
    actual = lkp[4:5]
    expect = 'bar'
    assertequal(expect, actual)
    
    actual = lkp[5:7]
    expect = 'bar'
    assertequal(expect, actual)
    
    actual = lkp[8:9]
    expect = 'baz'
    assertequal(expect, actual)
    
    actual = lkp[9:14]
    expect = None
    assertequal(expect, actual)
    
    actual = lkp[19:140]
    expect = None
    assertequal(expect, actual)
    
    actual = lkp[1]
    expect = None
    assertequal(expect, actual)
    
    actual = lkp[2]
    expect =  'foo'
    assertequal(expect, actual)
    
    actual = lkp[4]
    expect = 'bar'
    iassertequal(expect, actual)
    
    actual = lkp[5]
    expect = 'bar'
    iassertequal(expect, actual)
    
    actual = lkp[8]
    expect = 'baz'
    iassertequal(expect, actual)
    
    
def test_facetintervallookup():
    
    table = (('type', 'start', 'stop', 'value'),
             ('apple', 1, 4, 'foo'),
             ('apple', 3, 7, 'bar'),
             ('orange', 4, 9, 'baz'))
    
    lkp = facetintervallookup(table, key='type', start='start', stop='stop')

    actual = lkp['apple'][1:2]
    expect = [('apple', 1, 4, 'foo')]
    iassertequal(expect, actual)
    
    actual = lkp['apple'][2:4]
    expect = [('apple', 1, 4, 'foo'), ('apple', 3, 7, 'bar')]
    iassertequal(expect, actual)
    
    actual = lkp['apple'][2:5]
    expect = [('apple', 1, 4, 'foo'), ('apple', 3, 7, 'bar')]
    iassertequal(expect, actual)
    
    actual = lkp['orange'][2:5]
    expect = [('orange', 4, 9, 'baz')]
    iassertequal(expect, actual)
    
    actual = lkp['orange'][9:14]
    expect = []
    iassertequal(expect, actual)
    
    actual = lkp['orange'][19:140]
    expect = []
    iassertequal(expect, actual)
    
    actual = lkp['apple'][1]
    expect = []
    iassertequal(expect, actual)
    
    actual = lkp['apple'][2]
    expect = [('apple', 1, 4, 'foo')]
    iassertequal(expect, actual)
    
    actual = lkp['apple'][4]
    expect = [('apple', 3, 7, 'bar')]
    iassertequal(expect, actual)
    
    actual = lkp['apple'][5]
    expect = [('apple', 3, 7, 'bar')]
    iassertequal(expect, actual)
    
    actual = lkp['orange'][5]
    expect = [('orange', 4, 9, 'baz')]
    iassertequal(expect, actual)


def test_facetintervallookupone():
    
    table = (('type', 'start', 'stop', 'value'),
             ('apple', 1, 4, 'foo'),
             ('apple', 3, 7, 'bar'),
             ('orange', 4, 9, 'baz'))
    
    lkp = facetintervallookupone(table, key='type', start='start', stop='stop', valuespec='value')
    
    actual = lkp['apple'][1:2]
    expect = 'foo'
    assertequal(expect, actual)
    
    try:
        actual = lkp['apple'][2:4]
    except DuplicateKeyError:
        pass
    else:
        assert False, 'expected error'
    
    try:
        actual = lkp['apple'][2:5]
    except DuplicateKeyError:
        pass
    else:
        assert False, 'expected error'
    
    actual = lkp['apple'][4:5]
    expect = 'bar'
    assertequal(expect, actual)
    
    actual = lkp['orange'][4:5]
    expect = 'baz'
    assertequal(expect, actual)
    
    actual = lkp['apple'][5:7]
    expect = 'bar'
    assertequal(expect, actual)

    actual = lkp['orange'][5:7]
    expect = 'baz'
    assertequal(expect, actual)
    
    actual = lkp['apple'][8:9]
    expect = None
    assertequal(expect, actual)
    
    actual = lkp['orange'][8:9]
    expect = 'baz'
    assertequal(expect, actual)
    
    actual = lkp['orange'][9:14]
    expect = None
    assertequal(expect, actual)
    
    actual = lkp['orange'][19:140]
    expect = None
    assertequal(expect, actual)
    
    actual = lkp['apple'][1]
    expect = None
    assertequal(expect, actual)
    
    actual = lkp['apple'][2]
    expect =  'foo'
    assertequal(expect, actual)
    
    actual = lkp['apple'][4]
    expect = 'bar'
    assertequal(expect, actual)
    
    actual = lkp['apple'][5]
    expect = 'bar'
    assertequal(expect, actual)
    
    actual = lkp['orange'][5]
    expect = 'baz'
    assertequal(expect, actual)
    
    actual = lkp['apple'][8]
    expect = None
    assertequal(expect, actual)
    
    actual = lkp['orange'][8]
    expect = 'baz'
    assertequal(expect, actual)
    
    
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
    iassertequal(expect, actual)
    iassertequal(expect, actual)
    
    
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
    iassertequal(expect, actual)
    iassertequal(expect, actual)
    
    
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
    iassertequal(expect, actual)
    iassertequal(expect, actual)
    

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

    iassertequal(expect, actual)
    iassertequal(expect, actual)

               
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

    iassertequal(expect, actual)
    iassertequal(expect, actual)

                              