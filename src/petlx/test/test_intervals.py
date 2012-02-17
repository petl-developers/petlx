"""
TODO doc me

"""

from petl.testfun import iassertequal
from petl.util import DuplicateKeyError
from petl.testfun import assertequal

from petlx import intervallookup, intervallookupone


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
    iassertequal(expect, actual)
    
    try:
        actual = lkp[5]
    except DuplicateKeyError:
        pass
    else:
        assert False, 'expected error'
    
    actual = lkp[8]
    expect = 'baz'
    iassertequal(expect, actual)
    
    
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
    
    
    