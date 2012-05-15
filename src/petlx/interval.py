"""
Functions for working with intervals.

"""

from operator import itemgetter

from petlx.util import UnsatisfiedDependency
from petl.util import asindices, DuplicateKeyError, records, asdict
from petl.base import RowContainer
from petl.io import Uncacheable


dep_message = """
The package bx.intervals is required. Instructions for installation can be found 
at https://bitbucket.org/james_taylor/bx-python/wiki/Home or try pip install bx-python.
"""

try:
    import bx.intervals
except ImportError as e:
    raise UnsatisfiedDependency(e, dep_message)


def intervallookup(table, start='start', stop='stop', valuespec=None, 
                   proximity=0):
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

    .. versionadded:: 0.2
    
    """

    tree = bx.intervals.intersection.IntervalTree()
    it = iter(table)
    fields = it.next()
    assert start in fields, 'start field not recognised'
    assert stop in fields, 'stop field not recognised'
    getstart = itemgetter(fields.index(start))
    getstop = itemgetter(fields.index(stop))
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
    
            
def intervallookupone(table, start='start', stop='stop', valuespec=None, proximity=0, strict=True):
    """
    Construct an interval lookup for the given table, returning at most one
    result for each query. If ``strict=True`` is given, queries returning more
    than one result will raise a `DuplicateKeyError`. If ``strict=False`` is given,
    and there is more than one result, the first result is returned.
    
    See also :func:`intervallookup`.

    .. versionadded:: 0.2
    
    """

    tree = bx.intervals.intersection.IntervalTree()
    it = iter(table)
    fields = it.next()
    assert start in fields, 'start field not recognised'
    assert stop in fields, 'stop field not recognised'
    getstart = itemgetter(fields.index(start))
    getstop = itemgetter(fields.index(stop))
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
    
            
def intervalrecordlookup(table, start='start', stop='stop', proximity=0):
    """
    As :func:`intervallookup` but return records (dictionaries of values indexed
    by field name). 
    
    .. versionadded:: 0.2

    """

    tree = bx.intervals.intersection.IntervalTree()
    for rec in records(table):
        if start in rec and stop in rec:
            tree.add(rec[start], rec[stop], rec)
    return IntervalTreeWrapper(tree, proximity=proximity)


def intervalrecordlookupone(table, start='start', stop='stop', proximity=0, 
                            strict=True):
    """
    As :func:`intervallookupone` but return records (dictionaries of values indexed
    by field name).

    .. versionadded:: 0.2

    """

    tree = bx.intervals.intersection.IntervalTree()
    for rec in records(table):
        if start in rec and stop in rec:
            tree.add(rec[start], rec[stop], rec)
    return IntervalTreeReturnOneWrapper(tree, proximity=proximity, strict=strict)


def facetintervallookup(table, key, start='start', stop='stop', 
                        valuespec=None, proximity=0):
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
        
        >>> lkp = facetintervallookup(table, key='type', start='start', stop='stop')
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

    .. versionadded:: 0.2
    
    """
    
    it = iter(table)
    fields = it.next()
    assert start in fields, 'start field not recognised'
    assert stop in fields, 'stop field not recognised'
    getstart = itemgetter(fields.index(start))
    getstop = itemgetter(fields.index(stop))
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


def facetintervallookupone(table, key, start='start', stop='stop', 
                           valuespec=None, proximity=0, strict=True):
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
        
        >>> lkp = facetintervallookupone(table, key='type', start='start', stop='stop', valuespec='value')
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
    
    .. versionadded:: 0.2
    
    """
    
    it = iter(table)
    fields = it.next()
    assert start in fields, 'start field not recognised'
    assert stop in fields, 'stop field not recognised'
    getstart = itemgetter(fields.index(start))
    getstop = itemgetter(fields.index(stop))
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


def facetintervalrecordlookup(table, key, start='start', stop='stop', proximity=0):
    """
    As :func:`facetintervallookup` but return records (dictionaries of values indexed
    by field name). 
    
    .. versionadded:: 0.2

    """

    it = iter(table)
    fields = it.next()
    assert start in fields, 'start field not recognised'
    assert stop in fields, 'stop field not recognised'
    getstart = itemgetter(fields.index(start))
    getstop = itemgetter(fields.index(stop))
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


def facetintervalrecordlookupone(table, key, start, stop, proximity=0, strict=True):
    """
    As :func:`facetintervallookupone` but return records (dictionaries of values indexed
    by field name). 

    .. versionadded:: 0.2

    """
    
    it = iter(table)
    fields = it.next()
    assert start in fields, 'start field not recognised'
    assert stop in fields, 'stop field not recognised'
    getstart = itemgetter(fields.index(start))
    getstop = itemgetter(fields.index(stop))
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


def intervaljoin(left, right, lstart='start', lstop='stop', rstart='start',
                 rstop='stop', lfacet=None, rfacet=None, proximity=0):
    """
    Join two tables by overlapping intervals. E.g.::

        >>> from petl import look
        >>> from petlx.interval import intervaljoin
        >>> look(left)
        +---------+-------+--------+
        | 'begin' | 'end' | 'quux' |
        +=========+=======+========+
        | 1       | 2     | 'a'    |
        +---------+-------+--------+
        | 2       | 4     | 'b'    |
        +---------+-------+--------+
        | 2       | 5     | 'c'    |
        +---------+-------+--------+
        | 9       | 14    | 'd'    |
        +---------+-------+--------+
        | 9       | 140   | 'e'    |
        +---------+-------+--------+
        | 1       | 1     | 'f'    |
        +---------+-------+--------+
        | 2       | 2     | 'g'    |
        +---------+-------+--------+
        | 4       | 4     | 'h'    |
        +---------+-------+--------+
        | 5       | 5     | 'i'    |
        +---------+-------+--------+
        | 1       | 8     | 'j'    |
        +---------+-------+--------+
        
        >>> look(right)
        +---------+--------+---------+
        | 'start' | 'stop' | 'value' |
        +=========+========+=========+
        | 1       | 4      | 'foo'   |
        +---------+--------+---------+
        | 3       | 7      | 'bar'   |
        +---------+--------+---------+
        | 4       | 9      | 'baz'   |
        +---------+--------+---------+
        
        >>> result = intervaljoin(left, right, lstart='begin', lstop='end', rstart='start', rstop='stop')
        >>> look(result) 
        +---------+-------+--------+---------+--------+---------+
        | 'begin' | 'end' | 'quux' | 'start' | 'stop' | 'value' |
        +=========+=======+========+=========+========+=========+
        | 1       | 2     | 'a'    | 1       | 4      | 'foo'   |
        +---------+-------+--------+---------+--------+---------+
        | 2       | 4     | 'b'    | 1       | 4      | 'foo'   |
        +---------+-------+--------+---------+--------+---------+
        | 2       | 4     | 'b'    | 3       | 7      | 'bar'   |
        +---------+-------+--------+---------+--------+---------+
        | 2       | 5     | 'c'    | 1       | 4      | 'foo'   |
        +---------+-------+--------+---------+--------+---------+
        | 2       | 5     | 'c'    | 3       | 7      | 'bar'   |
        +---------+-------+--------+---------+--------+---------+
        | 2       | 5     | 'c'    | 4       | 9      | 'baz'   |
        +---------+-------+--------+---------+--------+---------+
        | 2       | 2     | 'g'    | 1       | 4      | 'foo'   |
        +---------+-------+--------+---------+--------+---------+
        | 4       | 4     | 'h'    | 3       | 7      | 'bar'   |
        +---------+-------+--------+---------+--------+---------+
        | 5       | 5     | 'i'    | 3       | 7      | 'bar'   |
        +---------+-------+--------+---------+--------+---------+
        | 5       | 5     | 'i'    | 4       | 9      | 'baz'   |
        +---------+-------+--------+---------+--------+---------+
    
    An additional key comparison can be added, e.g.::
    
        >>> from petl import look
        >>> from petlx.interval import intervaljoin    
        >>> look(left)
        +----------+---------+-------+
        | 'fruit'  | 'begin' | 'end' |
        +==========+=========+=======+
        | 'apple'  | 1       | 2     |
        +----------+---------+-------+
        | 'apple'  | 2       | 4     |
        +----------+---------+-------+
        | 'apple'  | 2       | 5     |
        +----------+---------+-------+
        | 'orange' | 2       | 5     |
        +----------+---------+-------+
        | 'orange' | 9       | 14    |
        +----------+---------+-------+
        | 'orange' | 19      | 140   |
        +----------+---------+-------+
        | 'apple'  | 1       | 1     |
        +----------+---------+-------+
        | 'apple'  | 2       | 2     |
        +----------+---------+-------+
        | 'apple'  | 4       | 4     |
        +----------+---------+-------+
        | 'apple'  | 5       | 5     |
        +----------+---------+-------+
        
        >>> look(right)
        +----------+---------+--------+---------+
        | 'type'   | 'start' | 'stop' | 'value' |
        +==========+=========+========+=========+
        | 'apple'  | 1       | 4      | 'foo'   |
        +----------+---------+--------+---------+
        | 'apple'  | 3       | 7      | 'bar'   |
        +----------+---------+--------+---------+
        | 'orange' | 4       | 9      | 'baz'   |
        +----------+---------+--------+---------+
        
        >>> result = intervaljoin(left, right, lstart='begin', lstop='end', rstart='start', rstop='stop', lfacet='fruit', rfacet='type')
        >>> look(result)
        +----------+---------+-------+----------+---------+--------+---------+
        | 'fruit'  | 'begin' | 'end' | 'type'   | 'start' | 'stop' | 'value' |
        +==========+=========+=======+==========+=========+========+=========+
        | 'apple'  | 1       | 2     | 'apple'  | 1       | 4      | 'foo'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'apple'  | 2       | 4     | 'apple'  | 1       | 4      | 'foo'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'apple'  | 2       | 4     | 'apple'  | 3       | 7      | 'bar'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'apple'  | 2       | 5     | 'apple'  | 1       | 4      | 'foo'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'apple'  | 2       | 5     | 'apple'  | 3       | 7      | 'bar'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'orange' | 2       | 5     | 'orange' | 4       | 9      | 'baz'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'apple'  | 2       | 2     | 'apple'  | 1       | 4      | 'foo'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'apple'  | 4       | 4     | 'apple'  | 3       | 7      | 'bar'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'apple'  | 5       | 5     | 'apple'  | 3       | 7      | 'bar'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'orange' | 5       | 5     | 'orange' | 4       | 9      | 'baz'   |
        +----------+---------+-------+----------+---------+--------+---------+
        
    .. versionadded:: 0.2
    
    """
    
    return IntervalJoinView(left, right, lstart=lstart, lstop=lstop,
                            rstart=rstart, rstop=rstop, lfacet=lfacet,
                            rfacet=rfacet, proximity=proximity)


class IntervalJoinView(RowContainer):
    
    def __init__(self, left, right, lstart='start', lstop='stop', 
                 rstart='start', rstop='stop', lfacet=None, rfacet=None,
                 proximity=0):
        self.left = left
        self.lstart = lstart
        self.lstop = lstop
        self.lfacet = lfacet
        self.right = right
        self.rstart = rstart
        self.rstop = rstop
        self.rfacet = rfacet
        self.proximity = proximity
        # TODO guard niether or both facet fields None

    def __iter__(self):
        return iterintervaljoin(self.left, self.right, self.lstart, self.lstop, 
                                self.rstart, self.rstop, self.lfacet, self.rfacet,
                                self.proximity)
        
    def cachetag(self):
        raise Uncacheable() # TODO
    

def iterintervaljoin(left, right, lstart, lstop, rstart, rstop, lfacet, rfacet,
                     proximity):

    # create iterators and obtain fields
    lit = iter(left)
    lfields = lit.next()
    assert lstart in lfields, 'field not found: %s' % lstart 
    assert lstop in lfields, 'field not found: %s' % lstop
    rit = iter(right)
    rfields = rit.next()
    assert rstart in rfields, 'field not found: %s' % rstart 
    assert rstop in rfields, 'field not found: %s' % rstop

    # determine output fields
    outfields = list(lfields)
    outfields.extend(rfields)
    yield tuple(outfields)
    
    # create getters for start and stop positions
    getlstart = itemgetter(lfields.index(lstart))
    getlstop = itemgetter(lfields.index(lstop))
     
    if rfacet is None:
        # build interval lookup for right table
        lookup = intervallookup(right, rstart, rstop, proximity=proximity)
        # main loop
        for lrow in lit:
            start = getlstart(lrow)
            stop = getlstop(lrow)
            rrows = lookup[start:stop]
            for rrow in rrows:
                outrow = list(lrow)
                outrow.extend(rrow)
                yield tuple(outrow)

    else:
        # build interval lookup for right table
        lookup = facetintervallookup(right, key=rfacet, start=rstart, stop=rstop,
                                     proximity=proximity)   
        # getter for facet key values in left table
        getlkey = itemgetter(*asindices(lfields, lfacet))
        # main loop
        for lrow in lit:
            lkey = getlkey(lrow)
            start = getlstart(lrow)
            stop = getlstop(lrow)
            try:
                rrows = lookup[lkey][start:stop]
            except AttributeError:
                pass
            else:
                for rrow in rrows:
                    outrow = list(lrow)
                    outrow.extend(rrow)
                    yield tuple(outrow)
            
            
def intervalleftjoin(left, right, lstart='start', lstop='stop', rstart='start',
                     rstop='stop', lfacet=None, rfacet=None, proximity=0,
                     missing=None):
    """
    Like :func:`intervaljoin` but rows from the left table without a match
    in the right table are also included. E.g.::

        >>> from petl import look
        >>> from petlx.interval import intervalleftjoin
        >>> look(left)
        +----------+---------+-------+
        | 'fruit'  | 'begin' | 'end' |
        +==========+=========+=======+
        | 'apple'  | 1       | 2     |
        +----------+---------+-------+
        | 'apple'  | 2       | 4     |
        +----------+---------+-------+
        | 'apple'  | 2       | 5     |
        +----------+---------+-------+
        | 'orange' | 2       | 5     |
        +----------+---------+-------+
        | 'orange' | 9       | 14    |
        +----------+---------+-------+
        | 'orange' | 19      | 140   |
        +----------+---------+-------+
        | 'apple'  | 1       | 1     |
        +----------+---------+-------+
        | 'apple'  | 2       | 2     |
        +----------+---------+-------+
        | 'apple'  | 4       | 4     |
        +----------+---------+-------+
        | 'apple'  | 5       | 5     |
        +----------+---------+-------+
        
        >>> look(right)
        +----------+---------+--------+---------+
        | 'type'   | 'start' | 'stop' | 'value' |
        +==========+=========+========+=========+
        | 'apple'  | 1       | 4      | 'foo'   |
        +----------+---------+--------+---------+
        | 'apple'  | 3       | 7      | 'bar'   |
        +----------+---------+--------+---------+
        | 'orange' | 4       | 9      | 'baz'   |
        +----------+---------+--------+---------+
        
        >>> result = intervalleftjoin(left, right, lstart='begin', lstop='end', rstart='start', rstop='stop')
        >>> look(result)
        +----------+---------+-------+----------+---------+--------+---------+
        | 'fruit'  | 'begin' | 'end' | 'type'   | 'start' | 'stop' | 'value' |
        +==========+=========+=======+==========+=========+========+=========+
        | 'apple'  | 1       | 2     | 'apple'  | 1       | 4      | 'foo'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'apple'  | 2       | 4     | 'apple'  | 1       | 4      | 'foo'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'apple'  | 2       | 4     | 'apple'  | 3       | 7      | 'bar'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'apple'  | 2       | 5     | 'apple'  | 1       | 4      | 'foo'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'apple'  | 2       | 5     | 'apple'  | 3       | 7      | 'bar'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'apple'  | 2       | 5     | 'orange' | 4       | 9      | 'baz'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'orange' | 2       | 5     | 'apple'  | 1       | 4      | 'foo'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'orange' | 2       | 5     | 'apple'  | 3       | 7      | 'bar'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'orange' | 2       | 5     | 'orange' | 4       | 9      | 'baz'   |
        +----------+---------+-------+----------+---------+--------+---------+
        | 'orange' | 9       | 14    | None     | None    | None   | None    |
        +----------+---------+-------+----------+---------+--------+---------+

    .. versionadded:: 0.2
    
    """
    
    return IntervalLeftJoinView(left, right, lstart=lstart, lstop=lstop,
                                rstart=rstart, rstop=rstop, lfacet=lfacet,
                                rfacet=rfacet, proximity=proximity, missing=missing)


class IntervalLeftJoinView(RowContainer):
    
    def __init__(self, left, right, lstart='start', lstop='stop', 
                 rstart='start', rstop='stop', lfacet=None, rfacet=None,
                 missing=None, proximity=0):
        self.left = left
        self.lstart = lstart
        self.lstop = lstop
        self.lfacet = lfacet
        self.right = right
        self.rstart = rstart
        self.rstop = rstop
        self.rfacet = rfacet
        self.missing = missing
        self.proximity = proximity
        # TODO guard niether or both facet fields None

    def __iter__(self):
        return iterintervalleftjoin(self.left, self.right, self.lstart, self.lstop, 
                                    self.rstart, self.rstop, self.lfacet, self.rfacet,
                                    self.proximity, self.missing)
        
    def cachetag(self):
        raise Uncacheable() # TODO
    

def iterintervalleftjoin(left, right, lstart, lstop, rstart, rstop, lfacet, rfacet,
                         proximity, missing):

    # create iterators and obtain fields
    lit = iter(left)
    lfields = lit.next()
    assert lstart in lfields, 'field not found: %s' % lstart 
    assert lstop in lfields, 'field not found: %s' % lstop
    rit = iter(right)
    rfields = rit.next()
    assert rstart in rfields, 'field not found: %s' % rstart 
    assert rstop in rfields, 'field not found: %s' % rstop

    # determine output fields
    outfields = list(lfields)
    outfields.extend(rfields)
    yield tuple(outfields)
    
    # create getters for start and stop positions
    getlstart = itemgetter(lfields.index(lstart))
    getlstop = itemgetter(lfields.index(lstop))

    if rfacet is None:
        # build interval lookup for right table
        lookup = intervallookup(right, rstart, rstop, proximity=proximity)
        # main loop
        for lrow in lit:
            start = getlstart(lrow)
            stop = getlstop(lrow)
            rrows = lookup[start:stop]
            if rrows:
                for rrow in rrows:
                    outrow = list(lrow)
                    outrow.extend(rrow)
                    yield tuple(outrow)
            else:
                outrow = list(lrow)
                outrow.extend([missing] * len(rfields))
                yield tuple(outrow)

    else:
        # build interval lookup for right table
        lookup = facetintervallookup(right, key=rfacet, start=rstart, stop=rstop,
                                     proximity=proximity)   
        # getter for facet key values in left table
        getlkey = itemgetter(*asindices(lfields, lfacet))
        # main loop
        for lrow in lit:
            lkey = getlkey(lrow)
            start = getlstart(lrow)
            stop = getlstop(lrow)
            
            try:
                rrows = lookup[lkey][start:stop]
            except AttributeError:
                rrows = None
                
            if rrows:
                for rrow in rrows:
                    outrow = list(lrow)
                    outrow.extend(rrow)
                    yield tuple(outrow)
            else:
                outrow = list(lrow)
                outrow.extend([missing] * len(rfields))
                yield tuple(outrow)


