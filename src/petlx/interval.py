"""
TODO doc me

"""

from operator import itemgetter
from petlx.util import UnsatisfiedDependency
from petl.util import asindices, DuplicateKeyError, records


dep_message = """
The package bx.intervals is required. Instructions for installation can be found 
at https://bitbucket.org/james_taylor/bx-python/wiki/Home or try pip install bx-python.
"""

try:
    import bx.intervals
except ImportError as e:
    raise UnsatisfiedDependency(e, dep_message)


def intervallookup(table, startf, stopf, valuespec=None, proximity=0):
    """
    Construct an interval lookup for the given table. E.g.::

        >>> from petlx import intervallookup    
        >>> table = [['start', 'stop', 'value'],
        ...          [1, 4, 'foo'],
        ...          [3, 7, 'bar'],
        ...          [4, 9, 'baz']]
        >>> lkp = intervallookup(table, 'start', 'stop')
        >>> lkp[1:2]
        [(1, 4, 'foo')]
        >>> lkp[2:4]
        [(1, 4, 'foo'), (3, 7, 'bar')]
        >>> lkp[2:5]
        [(1, 4, 'foo'), (3, 7, 'bar'), (4, 9, 'baz')]
        >>> lkp[9:14]
        []
        >>> lkp[19:140]
        []
        >>> lkp[1]
        []
        >>> lkp[2]
        [(1, 4, 'foo')]
        >>> lkp[4]
        [(3, 7, 'bar')]
        >>> lkp[5]
        [(3, 7, 'bar'), (4, 9, 'baz')]

    Note that there must be a non-zero overlap between the query and the interval
    for the interval to be retrieved, hence `lkp[1]` returns nothing. Use the 
    `proximity` keyword argument to find intervals within a given distance of
    the query.
    
    Some examples using the `proximity` and `valuespec` keyword arguments::
    
        >>> table = [['start', 'stop', 'value'],
        ...          [1, 4, 'foo'],
        ...          [3, 7, 'bar'],
        ...          [4, 9, 'baz']]
        >>> lkp = intervallookup(table, 'start', 'stop', valuespec='value', proximity=1)
        >>> lkp[1:2]
        ['foo']
        >>> lkp[2:4]
        ['foo', 'bar', 'baz']
        >>> lkp[2:5]
        ['foo', 'bar', 'baz']
        >>> lkp[9:14]
        ['baz']
        >>> lkp[19:140]
        []
        >>> lkp[1]
        ['foo']
        >>> lkp[2]
        ['foo']
        >>> lkp[4]
        ['foo', 'bar', 'baz']
        >>> lkp[5]
        ['bar', 'baz']
        >>> lkp[9]
        ['baz']

    The package bx.intervals is required. Instructions for installation can be found 
    at https://bitbucket.org/james_taylor/bx-python/wiki/Home or try ``pip install bx-python``.
    
    .. versionadded:: 0.2
    
    """

    tree = bx.intervals.intersection.IntervalTree()
    it = iter(table)
    fields = it.next()
    assert startf in fields, 'start field not recognised'
    assert stopf in fields, 'stop field not recognised'
    getstart = itemgetter(fields.index(startf))
    getstop = itemgetter(fields.index(stopf))
    if valuespec is None:
        valuespec = fields # default valuespec is complete row
    valueindices = asindices(fields, valuespec)
    assert len(valueindices) > 0, 'invalid valuespec'
    getvalue = itemgetter(*valueindices)
    for row in it:
        tree.add(getstart(row), getstop(row), getvalue(row))
    return IntervalTreeWrapper(tree, proximity=proximity)


class IntervalTreeWrapper(object):
    
    def __init__(self, tree, proximity=0):
        self.tree = tree
        self.proximity = proximity
        
    def __getitem__(self, item):
        if isinstance(item, (int, long, float)):
            start = item - self.proximity
            stop = item + self.proximity
        elif isinstance(item, slice):
            start = item.start - self.proximity
            stop = item.stop + self.proximity
        else:
            assert False, 'invalid item request'
        results = self.tree.find(start, stop)
        return results
            
            
def intervallookupone(table, startf, stopf, valuespec=None, proximity=0, strict=True):
    """
    Construct an interval lookup for the given table, returning at most one
    result for each query. If ``strict=True`` is given, queries returning more
    than one result will raise a `DuplicateKeyError`. If ``strict=False`` is given,
    and there is more than one result, the first result is returned.
    
    See also :func:`intervallookup`.

    The package bx.intervals is required. Instructions for installation can be found 
    at https://bitbucket.org/james_taylor/bx-python/wiki/Home or try ``pip install bx-python``.
    
    .. versionadded:: 0.2
    
    """

    tree = bx.intervals.intersection.IntervalTree()
    it = iter(table)
    fields = it.next()
    assert startf in fields, 'start field not recognised'
    assert stopf in fields, 'stop field not recognised'
    getstart = itemgetter(fields.index(startf))
    getstop = itemgetter(fields.index(stopf))
    if valuespec is None:
        valuespec = fields # default valuespec is complete row
    valueindices = asindices(fields, valuespec)
    assert len(valueindices) > 0, 'invalid valuespec'
    getvalue = itemgetter(*valueindices)
    for row in it:
        tree.add(getstart(row), getstop(row), getvalue(row))
    return IntervalTreeReturnOneWrapper(tree, proximity=proximity, strict=strict)


class IntervalTreeReturnOneWrapper(object):
    
    def __init__(self, tree, proximity=0, strict=True):
        self.tree = tree
        self.proximity = proximity
        self.strict = strict
        
    def __getitem__(self, item):
        if isinstance(item, (int, long, float)):
            start = item - self.proximity
            stop = item + self.proximity
        elif isinstance(item, slice):
            start = item.start - self.proximity
            stop = item.stop + self.proximity
        else:
            assert False, 'invalid item request'
        results = self.tree.find(start, stop)
        print results
        if len(results) == 0:
            return None
        elif len(results) > 1 and self.strict:
            raise DuplicateKeyError
        else:
            return results[0]


def intervalrecordlookup(table, startf, stopf, proximity=0):
    """
    As :func:`intervallookup` but return records (dictionaries of values indexed
    by field name). E.g.::

        >>> from petlx import intervalrecordlookup    
        >>> table = [['start', 'stop', 'value'],
        ...          [1, 4, 'foo'],
        ...          [3, 7, 'bar'],
        ...          [4, 9, 'baz']]
        >>> lkp = intervalrecordlookup(table, 'start', 'stop')
        >>> lkp[1:2]
        [{'start': 1, 'stop': 4, 'value': 'foo'}]
        >>> lkp[2:4]
        [{'start': 1, 'stop': 4, 'value': 'foo'}, {'start': 3, 'stop': 7, 'value': 'bar'}]
        >>> lkp[2:5]
        [{'start': 1, 'stop': 4, 'value': 'foo'}, {'start': 3, 'stop': 7, 'value': 'bar'}, {'start': 4, 'stop': 9, 'value': 'baz'}]
        >>> lkp[9:14]
        []
        >>> lkp[19:140]
        []
        >>> lkp[1]
        []
        >>> lkp[2]
        [{'start': 1, 'stop': 4, 'value': 'foo'}]
        >>> lkp[4]
        [{'start': 3, 'stop': 7, 'value': 'bar'}]
        >>> lkp[5]
        [{'start': 3, 'stop': 7, 'value': 'bar'}, {'start': 4, 'stop': 9, 'value': 'baz'}]

    The package bx.intervals is required. Instructions for installation can be found 
    at https://bitbucket.org/james_taylor/bx-python/wiki/Home or try ``pip install bx-python``.
    
    .. versionadded:: 0.2

    """

    tree = bx.intervals.intersection.IntervalTree()
    for rec in records(table):
        if startf in rec and stopf in rec:
            tree.add(rec[startf], rec[stopf], rec)
    return IntervalTreeWrapper(tree, proximity=proximity)


def intervalrecordlookupone(table, startf, stopf, proximity=0, strict=True):
    """
    As :func:`intervallookupone` but return records (dictionaries of values indexed
    by field name).

    The package bx.intervals is required. Instructions for installation can be found 
    at https://bitbucket.org/james_taylor/bx-python/wiki/Home or try ``pip install bx-python``.
    
    .. versionadded:: 0.2

    """

    tree = bx.intervals.intersection.IntervalTree()
    for rec in records(table):
        if startf in rec and stopf in rec:
            tree.add(rec[startf], rec[stopf], rec)
    return IntervalTreeReturnOneWrapper(tree, proximity=proximity, strict=strict)


            
            
