"""
Functions for working with intervals.

"""

from operator import itemgetter

from petlx.util import UnsatisfiedDependency
from petl.util import asindices, DuplicateKeyError, records, asdict


dep_message = """
The package bx.intervals is required. Instructions for installation can be found 
at https://bitbucket.org/james_taylor/bx-python/wiki/Home or try pip install bx-python.
"""

try:
    import bx.intervals
except ImportError as e:
    raise UnsatisfiedDependency(e, dep_message)


def intervallookup(table, startfield, stopfield, valuespec=None, proximity=0):
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
    assert startfield in fields, 'start field not recognised'
    assert stopfield in fields, 'stop field not recognised'
    getstart = itemgetter(fields.index(startfield))
    getstop = itemgetter(fields.index(stopfield))
    if valuespec is None:
        valuespec = fields # default valuespec is complete row
    valueindices = asindices(fields, valuespec)
    assert len(valueindices) > 0, 'invalid valuespec'
    getvalue = itemgetter(*valueindices)
    for row in it:
        tree.add(getstart(row), getstop(row), getvalue(row))
    return IntervalTreeWrapper(tree, proximity=proximity)


class IntervalTreeWrapper(object):
    
    def __init__(self, tree=None, proximity=0):
        if tree is None:
            self.tree = bx.intervals.intersection.IntervalTree()
        else:
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
            
    def __getattr__(self, attr):
        return getattr(self.tree, attr)
    
            
def intervallookupone(table, startfield, stopfield, valuespec=None, proximity=0, strict=True):
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
    assert startfield in fields, 'start field not recognised'
    assert stopfield in fields, 'stop field not recognised'
    getstart = itemgetter(fields.index(startfield))
    getstop = itemgetter(fields.index(stopfield))
    if valuespec is None:
        valuespec = fields # default valuespec is complete row
    valueindices = asindices(fields, valuespec)
    assert len(valueindices) > 0, 'invalid valuespec'
    getvalue = itemgetter(*valueindices)
    for row in it:
        tree.add(getstart(row), getstop(row), getvalue(row))
    return IntervalTreeReturnOneWrapper(tree, proximity=proximity, strict=strict)


class IntervalTreeReturnOneWrapper(object):
    
    def __init__(self, tree=None, proximity=0, strict=True):
        if tree is None:
            self.tree = bx.intervals.intersection.IntervalTree()
        else:
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
        if len(results) == 0:
            return None
        elif len(results) > 1 and self.strict:
            raise DuplicateKeyError
        else:
            return results[0]

    def __getattr__(self, attr):
        return getattr(self.tree, attr)
    
            
def intervalrecordlookup(table, startfield, stopfield, proximity=0):
    """
    As :func:`intervallookup` but return records (dictionaries of values indexed
    by field name). 
    
    The package bx.intervals is required. Instructions for installation can be found 
    at https://bitbucket.org/james_taylor/bx-python/wiki/Home or try ``pip install bx-python``.
    
    .. versionadded:: 0.2

    """

    tree = bx.intervals.intersection.IntervalTree()
    for rec in records(table):
        if startfield in rec and stopfield in rec:
            tree.add(rec[startfield], rec[stopfield], rec)
    return IntervalTreeWrapper(tree, proximity=proximity)


def intervalrecordlookupone(table, startfield, stopfield, proximity=0, strict=True):
    """
    As :func:`intervallookupone` but return records (dictionaries of values indexed
    by field name).

    The package bx.intervals is required. Instructions for installation can be found 
    at https://bitbucket.org/james_taylor/bx-python/wiki/Home or try ``pip install bx-python``.
    
    .. versionadded:: 0.2

    """

    tree = bx.intervals.intersection.IntervalTree()
    for rec in records(table):
        if startfield in rec and stopfield in rec:
            tree.add(rec[startfield], rec[stopfield], rec)
    return IntervalTreeReturnOneWrapper(tree, proximity=proximity, strict=strict)


def facetintervallookup(table, key, startfield, stopfield, valuespec=None, proximity=0):
    """
    Construct a faceted interval lookup for the given table. E.g.::

        >>> from petl import look
        >>> from petlx.interval import facetintervallookup
        >>> look(table)
        +----------+---------+--------+---------+
        | 'type'   | 'start' | 'stop' | 'value' |
        +==========+=========+========+=========+
        | 'apple'  | 1       | 4      | 'foo'   |
        +----------+---------+--------+---------+
        | 'apple'  | 3       | 7      | 'bar'   |
        +----------+---------+--------+---------+
        | 'orange' | 4       | 9      | 'baz'   |
        +----------+---------+--------+---------+
        
        >>> lkp = facetintervallookup(table, key='type', startfield='start', stopfield='stop')
        >>> lkp['apple'][1:2]
        [('apple', 1, 4, 'foo')]
        >>> lkp['apple'][2:4]
        [('apple', 1, 4, 'foo'), ('apple', 3, 7, 'bar')]
        >>> lkp['apple'][2:5]
        [('apple', 1, 4, 'foo'), ('apple', 3, 7, 'bar')]
        >>> lkp['orange'][2:5]
        [('orange', 4, 9, 'baz')]
        >>> lkp['orange'][9:14]
        []
        >>> lkp['orange'][19:140]
        []
        >>> lkp['apple'][1]
        []
        >>> lkp['apple'][2]
        [('apple', 1, 4, 'foo')]
        >>> lkp['apple'][4]
        [('apple', 3, 7, 'bar')]
        >>> lkp['apple'][5]
        [('apple', 3, 7, 'bar')]
        >>> lkp['orange'][5]
        [('orange', 4, 9, 'baz')]

    The package bx.intervals is required. Instructions for installation can be found 
    at https://bitbucket.org/james_taylor/bx-python/wiki/Home or try ``pip install bx-python``.
        
    .. versionadded:: 0.2
    
    """
    
    it = iter(table)
    fields = it.next()
    assert startfield in fields, 'start field not recognised'
    assert stopfield in fields, 'stop field not recognised'
    getstart = itemgetter(fields.index(startfield))
    getstop = itemgetter(fields.index(stopfield))
    if valuespec is None:
        valuespec = fields # default valuespec is complete row
    valueindices = asindices(fields, valuespec)
    assert len(valueindices) > 0, 'invalid valuespec'
    getvalue = itemgetter(*valueindices)
    keyindices = asindices(fields, key)
    assert len(keyindices) > 0, 'invalid key'
    getkey = itemgetter(*keyindices)

    trees = dict()
    for row in it:
        k = getkey(row)
        if k not in trees:
            trees[k] = IntervalTreeWrapper(proximity=proximity)
        trees[k].add(getstart(row), getstop(row), getvalue(row))
    return trees


def facetintervallookupone(table, key, startfield, stopfield, valuespec=None, proximity=0, strict=True):
    """
    Construct a faceted interval lookup for the given table, returning at most one
    result for each query, e.g.::
    
        >>> from petl import look
        >>> from petlx.interval import facetintervallookupone
        >>> look(table)
        +----------+---------+--------+---------+
        | 'type'   | 'start' | 'stop' | 'value' |
        +==========+=========+========+=========+
        | 'apple'  | 1       | 4      | 'foo'   |
        +----------+---------+--------+---------+
        | 'apple'  | 3       | 7      | 'bar'   |
        +----------+---------+--------+---------+
        | 'orange' | 4       | 9      | 'baz'   |
        +----------+---------+--------+---------+
        
        >>> lkp = facetintervallookupone(table, key='type', startfield='start', stopfield='stop', valuespec='value')
        >>> lkp['apple'][1:2]
        'foo'
        >>> lkp['apple'][2:4]
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "petlx/interval.py", line 191, in __getitem__
            raise DuplicateKeyError
        petl.util.DuplicateKeyError
        >>> lkp['apple'][2:5]
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "petlx/interval.py", line 191, in __getitem__
            raise DuplicateKeyError
        petl.util.DuplicateKeyError
        >>> lkp['apple'][4:5]
        'bar'
        >>> lkp['orange'][4:5]
        'baz'
        >>> lkp['apple'][5:7]
        'bar'
        >>> lkp['orange'][5:7]
        'baz'
        >>> lkp['apple'][8:9]
        >>> lkp['orange'][8:9]
        'baz'
        >>> lkp['orange'][9:14]
        >>> lkp['orange'][19:140]
        >>> lkp['apple'][1]
        >>> lkp['apple'][2]
        'foo'
        >>> lkp['apple'][4]
        'bar'
        >>> lkp['apple'][5]
        'bar'
        >>> lkp['orange'][5]
        'baz'
        >>> lkp['apple'][8]
        >>> lkp['orange'][8]
        'baz'
    
    
    If ``strict=True`` is given, queries returning more
    than one result will raise a `DuplicateKeyError`. If ``strict=False`` is given,
    and there is more than one result, the first result is returned.
    
    See also :func:`facetintervallookup`.

    The package bx.intervals is required. Instructions for installation can be found 
    at https://bitbucket.org/james_taylor/bx-python/wiki/Home or try ``pip install bx-python``.
    
    .. versionadded:: 0.2
    
    """
    
    it = iter(table)
    fields = it.next()
    assert startfield in fields, 'start field not recognised'
    assert stopfield in fields, 'stop field not recognised'
    getstart = itemgetter(fields.index(startfield))
    getstop = itemgetter(fields.index(stopfield))
    if valuespec is None:
        valuespec = fields # default valuespec is complete row
    valueindices = asindices(fields, valuespec)
    assert len(valueindices) > 0, 'invalid valuespec'
    getvalue = itemgetter(*valueindices)
    keyindices = asindices(fields, key)
    assert len(keyindices) > 0, 'invalid key'
    getkey = itemgetter(*keyindices)

    trees = dict()
    for row in it:
        k = getkey(row)
        if k not in trees:
            trees[k] = IntervalTreeReturnOneWrapper(proximity=proximity, strict=strict)
        trees[k].add(getstart(row), getstop(row), getvalue(row))
    return trees


def facetintervalrecordlookup(table, key, startfield, stopfield, proximity=0):
    """
    As :func:`facetintervallookup` but return records (dictionaries of values indexed
    by field name). 

    The package bx.intervals is required. Instructions for installation can be found 
    at https://bitbucket.org/james_taylor/bx-python/wiki/Home or try ``pip install bx-python``.
    
    .. versionadded:: 0.2

    """

    it = iter(table)
    fields = it.next()
    assert startfield in fields, 'start field not recognised'
    assert stopfield in fields, 'stop field not recognised'
    getstart = itemgetter(fields.index(startfield))
    getstop = itemgetter(fields.index(stopfield))
    keyindices = asindices(fields, key)
    assert len(keyindices) > 0, 'invalid key'
    getkey = itemgetter(*keyindices)

    trees = dict()
    for row in it:
        k = getkey(row)
        if k not in trees:
            trees[k] = IntervalTreeWrapper(proximity=proximity)
        trees[k].add(getstart(row), getstop(row), asdict(fields, row))
    return trees


def facetintervalrecordlookupone(table, key, startfield, stopfield, proximity=0, strict=True):
    """
    As :func:`facetintervallookupone` but return records (dictionaries of values indexed
    by field name). 

    The package bx.intervals is required. Instructions for installation can be found 
    at https://bitbucket.org/james_taylor/bx-python/wiki/Home or try ``pip install bx-python``.
    
    .. versionadded:: 0.2

    """
    
    it = iter(table)
    fields = it.next()
    assert startfield in fields, 'start field not recognised'
    assert stopfield in fields, 'stop field not recognised'
    getstart = itemgetter(fields.index(startfield))
    getstop = itemgetter(fields.index(stopfield))
    keyindices = asindices(fields, key)
    assert len(keyindices) > 0, 'invalid key'
    getkey = itemgetter(*keyindices)

    trees = dict()
    for row in it:
        k = getkey(row)
        if k not in trees:
            trees[k] = IntervalTreeReturnOneWrapper(proximity=proximity, strict=strict)
        trees[k].add(getstart(row), getstop(row), asdict(fields, row))
    return trees

