"""
Functions for working with intervals.

"""

from operator import itemgetter, attrgetter

from petlx.util import UnsatisfiedDependency
from petl.util import asindices, DuplicateKeyError, records, \
    RowContainer, values, rowgroupby
from petl.transform import addfield, sort


dep_message = """
The package bx.intervals is required. Instructions for installation can be found 
at https://bitbucket.org/james_taylor/bx-python/wiki/Home or try pip install bx-python.
"""


def tupletree(table, start='start', stop='stop', value=None):
    """
    Construct an interval tree for the given table, where each node in the tree is a row of the table.

    """

    try:
        import bx.intervals
    except ImportError as e:
        raise UnsatisfiedDependency(e, dep_message)

    tree = bx.intervals.intersection.IntervalTree()
    it = iter(table)
    fields = it.next()
    assert start in fields, 'start field not recognised'
    assert stop in fields, 'stop field not recognised'
    getstart = itemgetter(fields.index(start))
    getstop = itemgetter(fields.index(stop))
    if value is None:
        getvalue = tuple
    else:
        valueindices = asindices(fields, value)
        assert len(valueindices) > 0, 'invalid value field specification'
        getvalue = itemgetter(*valueindices)
    for row in it:
        tree.add(getstart(row), getstop(row), getvalue(row))
    return tree


def tupletrees(table, facet, start='start', stop='stop', value=None):
    """
    Construct faceted interval trees for the given table, where each node in the tree is a row of the table.

    """

    try:
        import bx.intervals
    except ImportError as e:
        raise UnsatisfiedDependency(e, dep_message)

    it = iter(table)
    fields = it.next()
    assert start in fields, 'start field not recognised'
    assert stop in fields, 'stop field not recognised'
    getstart = itemgetter(fields.index(start))
    getstop = itemgetter(fields.index(stop))
    if value is None:
        getvalue = tuple
    else:
        valueindices = asindices(fields, value)
        assert len(valueindices) > 0, 'invalid value field specification'
        getvalue = itemgetter(*valueindices)
    keyindices = asindices(fields, facet)
    assert len(keyindices) > 0, 'invalid key'
    getkey = itemgetter(*keyindices)

    trees = dict()
    for row in it:
        k = getkey(row)
        if k not in trees:
            trees[k] = bx.intervals.intersection.IntervalTree()
        trees[k].add(getstart(row), getstop(row), getvalue(row))
    return trees


def recordtree(table, start='start', stop='stop'):
    """
    Construct an interval tree for the given table, where each node in the tree is a row of the table represented
    as a hybrid tuple/dictionary-style record object.

    """

    try:
        import bx.intervals
    except ImportError as e:
        raise UnsatisfiedDependency(e, dep_message)

    getstart = attrgetter(start)
    getstop = attrgetter(stop)

    tree = bx.intervals.intersection.IntervalTree()
    for rec in records(table):
        tree.add(getstart(rec), getstop(rec), rec)


def recordtrees(table, facet, start='start', stop='stop'):
    """
    Construct faceted interval trees for the given table, where each node in the tree is a row of the table represented
    as a hybrid tuple/dictionary-style record object.

    """

    try:
        import bx.intervals
    except ImportError as e:
        raise UnsatisfiedDependency(e, dep_message)

    getstart = attrgetter(start)
    getstop = attrgetter(stop)
    getkey = attrgetter(facet)

    trees = dict()
    for rec in records(table):
        k = getkey(rec)
        if k not in trees:
            trees[k] = bx.intervals.intersection.IntervalTree()
        trees[k].add(getstart(rec), getstop(rec), rec)
    return trees


def intervallookup(table, start='start', stop='stop', value=None,
                   proximity=0):
    """
    Construct an interval lookup for the given table. E.g.::

        >>> from petlx.interval import intervallookup    
        >>> table = [['start', 'stop', 'value'],
        ...          [1, 4, 'foo'],
        ...          [3, 7, 'bar'],
        ...          [4, 9, 'baz']]
        >>> lkp = intervallookup(table, 'start', 'stop')
        >>> lkp.find(1, 2)
        [(1, 4, 'foo')]
        >>> lkp.find(2, 4)
        [(1, 4, 'foo'), (3, 7, 'bar')]
        >>> lkp.find(2, 5)
        [(1, 4, 'foo'), (3, 7, 'bar'), (4, 9, 'baz')]
        >>> lkp.find(9, 14)
        []
        >>> lkp.find(19, 140)
        []
        >>> lkp.find(1)
        []
        >>> lkp.find(2)
        [(1, 4, 'foo')]
        >>> lkp.find(4)
        [(3, 7, 'bar')]
        >>> lkp.find(5)
        [(3, 7, 'bar'), (4, 9, 'baz')]

    Note that there must be a non-zero overlap between the query and the interval
    for the interval to be retrieved, hence `lkp.find(1)` returns nothing. Use the
    `proximity` keyword argument to find intervals within a given distance of
    the query.
    
    Some examples using the `proximity` and `value` keyword arguments::
    
        >>> table = [['start', 'stop', 'value'],
        ...          [1, 4, 'foo'],
        ...          [3, 7, 'bar'],
        ...          [4, 9, 'baz']]
        >>> lkp = intervallookup(table, 'start', 'stop', value='value', proximity=1)
        >>> lkp.find(1, 2)
        ['foo']
        >>> lkp.find(2, 4)
        ['foo', 'bar', 'baz']
        >>> lkp.find(2, 5)
        ['foo', 'bar', 'baz']
        >>> lkp.find(9, 14)
        ['baz']
        >>> lkp.find(19, 140)
        []
        >>> lkp.find(1)
        ['foo']
        >>> lkp.find(2)
        ['foo']
        >>> lkp.find(4)
        ['foo', 'bar', 'baz']
        >>> lkp.find(5)
        ['bar', 'baz']
        >>> lkp.find(9)
        ['baz']

    .. versionadded:: 0.2
    
    """

    tree = tupletree(table, start=start, stop=stop, value=value)
    return IntervalTreeLookup(tree, proximity=proximity)


class IntervalTreeLookup(object):
    
    def __init__(self, tree=None, proximity=0):
        try:
            import bx.intervals
        except ImportError as e:
            raise UnsatisfiedDependency(e, dep_message)
        if tree is None:
            self.tree = bx.intervals.intersection.IntervalTree()
        else:
            self.tree = tree
        self.proximity = proximity

    def find(self, start, stop=None):
        if stop is None:
            stop = start + self.proximity
        else:
            stop = stop + self.proximity
        start = start - self.proximity
        return self.tree.find(start, stop)
        
    def __getitem__(self, item):
        # maintain for backwards compatibility but this usage is deprecated
        # use find() instead
        if isinstance(item, (int, long, float)):
            return self.find(item)
        elif isinstance(item, slice):
            return self.find(item.start, item.stop)
        else:
            raise Exception('invalid item request')


def intervallookupone(table, start='start', stop='stop', value=None, proximity=0, strict=True):
    """
    Construct an interval lookup for the given table, returning at most one
    result for each query. If ``strict=True`` is given, queries returning more
    than one result will raise a `DuplicateKeyError`. If ``strict=False`` is given,
    and there is more than one result, the first result is returned.
    
    See also :func:`intervallookup`.

    .. versionadded:: 0.2
    
    """

    tree = tupletree(table, start=start, stop=stop, value=value)
    return IntervalTreeLookupOne(tree, proximity=proximity, strict=strict)


class IntervalTreeLookupOne(object):
    
    def __init__(self, tree=None, proximity=0, strict=True):
        try:
            import bx.intervals
        except ImportError as e:
            raise UnsatisfiedDependency(e, dep_message)
        if tree is None:
            self.tree = bx.intervals.intersection.IntervalTree()
        else:
            self.tree = tree
        self.proximity = proximity
        self.strict = strict
        
    def find(self, start, stop=None):
        if stop is None:
            stop = start + self.proximity
        else:
            stop = stop + self.proximity
        start = start - self.proximity
        results = self.tree.find(start, stop)
        if len(results) == 0:
            return None
        elif len(results) > 1 and self.strict:
            raise DuplicateKeyError
        else:
            return results[0]

    def __getitem__(self, item):
        # maintain for backwards compatibility but this usage is deprecated
        # use find() instead
        if isinstance(item, (int, long, float)):
            return self.find(item)
        elif isinstance(item, slice):
            return self.find(item.start, item.stop)
        else:
            raise Exception('invalid item request')


def intervalrecordlookup(table, start='start', stop='stop', proximity=0):
    """
    As :func:`intervallookup` but return records.
    
    .. versionadded:: 0.2

    """

    tree = recordtree(table, start=start, stop=stop)
    return IntervalTreeLookup(tree, proximity=proximity)


def intervalrecordlookupone(table, start='start', stop='stop', proximity=0, 
                            strict=True):
    """
    As :func:`intervallookupone` but return records.

    .. versionadded:: 0.2

    """

    tree = recordtree(table, start=start, stop=stop)
    return IntervalTreeLookupOne(tree, proximity=proximity, strict=strict)


def facetintervallookup(table, facet, start='start', stop='stop',
                        value=None, proximity=0):
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
        
        >>> lkp = facetintervallookup(table, facet='type', start='start', stop='stop')
        >>> lkp['apple'].find(1, 2)
        [('apple', 1, 4, 'foo')]
        >>> lkp['apple'].find(2, 4)
        [('apple', 1, 4, 'foo'), ('apple', 3, 7, 'bar')]
        >>> lkp['apple'].find(2, 5)
        [('apple', 1, 4, 'foo'), ('apple', 3, 7, 'bar')]
        >>> lkp['orange'].find(2, 5)
        [('orange', 4, 9, 'baz')]
        >>> lkp['orange'].find(9, 14)
        []
        >>> lkp['orange'].find(19, 140)
        []
        >>> lkp['apple'].find(1)
        []
        >>> lkp['apple'].find(2)
        [('apple', 1, 4, 'foo')]
        >>> lkp['apple'].find(4)
        [('apple', 3, 7, 'bar')]
        >>> lkp['apple'].find(5)
        [('apple', 3, 7, 'bar')]
        >>> lkp['orange'].find(5)
        [('orange', 4, 9, 'baz')]

    .. versionadded:: 0.2
    
    """

    trees = tupletrees(table, facet, start=start, stop=stop, value=value)
    for k in trees:
        trees[k] = IntervalTreeLookup(trees[k], proximity=proximity)
    return trees


def facetintervallookupone(table, facet, start='start', stop='stop',
                           value=None, proximity=0, strict=True):
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
        
        >>> lkp = facetintervallookupone(table, key='type', start='start', stop='stop', value='value')
        >>> lkp['apple'].find(1, 2)
        'foo'
        >>> lkp['apple'].find(2, 4)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "petlx/interval.py", line 191, in __getitem__
            raise DuplicateKeyError
        petl.util.DuplicateKeyError
        >>> lkp['apple'].find(2, 5)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "petlx/interval.py", line 191, in __getitem__
            raise DuplicateKeyError
        petl.util.DuplicateKeyError
        >>> lkp['apple'].find(4, 5)
        'bar'
        >>> lkp['orange'].find(4, 5)
        'baz'
        >>> lkp['apple'].find(5, 7)
        'bar'
        >>> lkp['orange'].find(5, 7)
        'baz'
        >>> lkp['apple'].find(8, 9)
        >>> lkp['orange'].find(8, 9)
        'baz'
        >>> lkp['orange'].find(9, 14)
        >>> lkp['orange'].find(19, 140)
        >>> lkp['apple'].find(1)
        >>> lkp['apple'].find(2)
        'foo'
        >>> lkp['apple'].find(4)
        'bar'
        >>> lkp['apple'].find(5)
        'bar'
        >>> lkp['orange'].find(5)
        'baz'
        >>> lkp['apple'].find(8)
        >>> lkp['orange'].find(8)
        'baz'
    
    
    If ``strict=True`` is given, queries returning more
    than one result will raise a `DuplicateKeyError`. If ``strict=False`` is given,
    and there is more than one result, the first result is returned.
    
    See also :func:`facetintervallookup`.
    
    .. versionadded:: 0.2
    
    """
    
    trees = tupletrees(table, facet, start=start, stop=stop, value=value)
    for k in trees:
        trees[k] = IntervalTreeLookupOne(trees[k], proximity=proximity, strict=strict)
    return trees


def facetintervalrecordlookup(table, facet, start='start', stop='stop', proximity=0):
    """
    As :func:`facetintervallookup` but return records.
    
    .. versionadded:: 0.2

    """

    trees = recordtrees(table, facet, start=start, stop=stop)
    for k in trees:
        trees[k] = IntervalTreeLookup(trees[k], proximity=proximity)
    return trees


def facetintervalrecordlookupone(table, facet, start, stop, proximity=0, strict=True):
    """
    As :func:`facetintervallookupone` but return records.

    .. versionadded:: 0.2

    """
    
    trees = recordtrees(table, facet, start=start, stop=stop)
    for k in trees:
        trees[k] = IntervalTreeLookup(trees[k], proximity=proximity, strict=strict)
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
    
    assert (lfacet is None) == (rfacet is None), 'facet key field must be provided for both or neither table'
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
        

def iterintervaljoin(left, right, lstart, lstop, rstart, rstop, lfacet, rfacet,
                     proximity):

    # create iterators and obtain fields
    lit = iter(left)
    lfields = lit.next()
    assert lstart in lfields, 'field not found: %s' % lstart 
    assert lstop in lfields, 'field not found: %s' % lstop
    if lfacet is not None:
        assert lfacet in lfields, 'field not found: %s' % lfacet
    rit = iter(right)
    rfields = rit.next()
    assert rstart in rfields, 'field not found: %s' % rstart 
    assert rstop in rfields, 'field not found: %s' % rstop
    if rfacet is not None:
        assert rfacet in rfields, 'field not found: %s' % rfacet

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
        find = lookup.find
        # main loop
        for lrow in lit:
            start = getlstart(lrow)
            stop = getlstop(lrow)
            rrows = find(start, stop)
            for rrow in rrows:
                outrow = list(lrow)
                outrow.extend(rrow)
                yield tuple(outrow)

    else:
        # build interval lookup for right table
        lookup = facetintervallookup(right, facet=rfacet, start=rstart, stop=rstop,
                                     proximity=proximity)
        find = dict()
        for f in lookup:
            find[f] = lookup[f].find
        # getter for facet key values in left table
        getlkey = itemgetter(*asindices(lfields, lfacet))
        # main loop
        for lrow in lit:
            lkey = getlkey(lrow)
            start = getlstart(lrow)
            stop = getlstop(lrow)
            try:
                rrows = find[lkey](start, stop)
            except KeyError:
                pass
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
    
    assert (lfacet is None) == (rfacet is None), 'facet key field must be provided for both or neither table'
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

    def __iter__(self):
        return iterintervalleftjoin(self.left, self.right, self.lstart, self.lstop, 
                                    self.rstart, self.rstop, self.lfacet, self.rfacet,
                                    self.proximity, self.missing)
        

def iterintervalleftjoin(left, right, lstart, lstop, rstart, rstop, lfacet, rfacet,
                         proximity, missing):

    # create iterators and obtain fields
    lit = iter(left)
    lfields = lit.next()
    assert lstart in lfields, 'field not found: %s' % lstart 
    assert lstop in lfields, 'field not found: %s' % lstop
    if lfacet is not None:
        assert lfacet in lfields, 'field not found: %s' % lfacet
    rit = iter(right)
    rfields = rit.next()
    assert rstart in rfields, 'field not found: %s' % rstart 
    assert rstop in rfields, 'field not found: %s' % rstop
    if rfacet is not None:
        assert rfacet in rfields, 'field not found: %s' % rfacet

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
        find = lookup.find
        # main loop
        for lrow in lit:
            start = getlstart(lrow)
            stop = getlstop(lrow)
            rrows = find(start, stop)
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
        lookup = facetintervallookup(right, facet=rfacet, start=rstart, stop=rstop,
                                     proximity=proximity)   
        find = dict()
        for f in lookup:
            find[f] = lookup[f].find
        # getter for facet key values in left table
        getlkey = itemgetter(*asindices(lfields, lfacet))
        # main loop
        for lrow in lit:
            lkey = getlkey(lrow)
            start = getlstart(lrow)
            stop = getlstop(lrow)
            
            try:
                rrows = find[lkey](start, stop)
            except KeyError:
                rrows = None
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


def intervaljoinvalues(left, right, value, lstart='start', lstop='stop', rstart='start',
                       rstop='stop', lfacet=None, rfacet=None, proximity=0):
    """
    Convenience function to join the left table with values from a specific 
    field in the right hand table.
    
    .. versionadded:: 0.5.3
    
    """
    
    assert (lfacet is None) == (rfacet is None), 'facet key field must be provided for both or neither table'
    if lfacet is None:
        lkp = intervallookup(right, start=rstart, stop=rstop, value=value, proximity=proximity)
        f = lambda row: lkp.find(row[lstart], row[lstop])
    else:
        lkp = facetintervallookup(right, rfacet, start=rstart, stop=rstop, value=value, proximity=proximity)
        f = lambda row: lkp[row[lfacet]].find(row[lstart], row[lstop])
    return addfield(left, value, f)
        
        
def intervalsubtract(left, right, lstart='start', lstop='stop', rstart='start',
                     rstop='stop', lfacet=None, rfacet=None, proximity=0):
    """
    Subtract intervals in the right hand table from intervals in the left hand 
    table.
    
    .. versionadded:: 0.5.4
    
    """

    assert (lfacet is None) == (rfacet is None), 'facet key field must be provided for both or neither table'
    return IntervalSubtractView(left, right, lstart=lstart, lstop=lstop,
                                rstart=rstart, rstop=rstop, lfacet=lfacet,
                                rfacet=rfacet, proximity=proximity)


class IntervalSubtractView(RowContainer):
    
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

    def __iter__(self):
        return iterintervalsubtract(self.left, self.right, self.lstart, self.lstop, 
                                    self.rstart, self.rstop, self.lfacet, self.rfacet,
                                    self.proximity)
        

def iterintervalsubtract(left, right, lstart, lstop, rstart, rstop, lfacet, rfacet,
                         proximity):

    # create iterators and obtain fields
    lit = iter(left)
    lfields = lit.next()
    assert lstart in lfields, 'field not found: %s' % lstart 
    assert lstop in lfields, 'field not found: %s' % lstop
    if lfacet is not None:
        assert lfacet in lfields, 'field not found: %s' % lfacet
    rit = iter(right)
    rfields = rit.next()
    assert rstart in rfields, 'field not found: %s' % rstart 
    assert rstop in rfields, 'field not found: %s' % rstop
    if rfacet is not None:
        assert rfacet in rfields, 'field not found: %s' % rfacet

    # determine output fields
    outfields = list(lfields)
#    outfields.extend(rfields)
    yield tuple(outfields)
    
    # create getters for start and stop positions
    lstartidx = lfields.index(lstart)
    lstopidx = lfields.index(lstop)
    getlcoords = itemgetter(lstartidx, lstopidx)
    getrcoords = itemgetter(rfields.index(rstart), rfields.index(rstop))

    if rfacet is None:
        # build interval lookup for right table
        lookup = intervallookup(right, rstart, rstop, proximity=proximity)
        find = lookup.find
        # main loop
        for lrow in lit:
            start, stop = getlcoords(lrow)
            rrows = find(start, stop)
            if not rrows:
                yield tuple(lrow)
            else:
                rivs = sorted([getrcoords(rrow) for rrow in rrows], key=itemgetter(0))  # sort by start
                for x, y in _subtract(start, stop, rivs):
                    out = list(lrow)
                    out[lstartidx] = x
                    out[lstopidx] = y
                    yield tuple(out)
                
    else:
        # build interval lookup for right table
        lookup = facetintervallookup(right, facet=rfacet, start=rstart, stop=rstop,
                                     proximity=proximity)   
        # getter for facet key values in left table
        getlkey = itemgetter(*asindices(lfields, lfacet))
        # main loop
        for lrow in lit:
            lkey = getlkey(lrow)
            start, stop = getlcoords(lrow)
            try:
                rrows = lookup[lkey].find(start, stop)
            except KeyError:
                rrows = None
            except AttributeError:
                rrows = None
            if not rrows:
                yield tuple(lrow)
            else:
                rivs = sorted([getrcoords(rrow) for rrow in rrows], key=itemgetter(0))  # sort by start
                for x, y in _subtract(start, stop, rivs):
                    out = list(lrow)
                    out[lstartidx] = x
                    out[lstopidx] = y
                    yield tuple(out)


from collections import namedtuple
_Interval = namedtuple('Interval', 'start stop')


def collapsedintervals(tbl, start='start', stop='stop', facet=None):
    """
    Utility function to collapse intervals in a table. 
    
    If no facet key is given, returns an iterator over `(start, stop)` tuples.
    
    If facet key is given, returns an iterator over `(key, start, stop)` tuples.  
    
    .. versionadded:: 0.5.5
    
    """
    
    if facet is None:
        tbl = sort(tbl, key=start)
        for iv in _collapse(values(tbl, (start, stop))):
            yield iv
    else:
        tbl = sort(tbl, key=(facet, start))
        for k, g in rowgroupby(tbl, key=facet, value=(start, stop)):
            for iv in _collapse(g):
                yield (k,) + iv


def _collapse(intervals):
    """
    Collapse an iterable of intervals sorted by start coord.
    
    """
    span = None
    for start, stop in intervals:
        if span is None:
            span = _Interval(start, stop)
        elif start <= span.stop < stop:
            span = _Interval(span.start, stop)
        elif start > span.stop:
            yield span
            span = _Interval(start, stop)
    if span is not None:
        yield span
    
    
def _subtract(start, stop, intervals):
    """
    Subtract intervals from a spanning interval.
    
    """
    remainder_start = start
    sub_stop = None
    for sub_start, sub_stop in _collapse(intervals):
        if remainder_start < sub_start:
            yield _Interval(remainder_start, sub_start)
        remainder_start = sub_stop
    if sub_stop is not None and sub_stop < stop:
        yield _Interval(sub_stop, stop)
    

import sys
from petlx.integration import integrate
integrate(sys.modules[__name__])

