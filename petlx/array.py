"""
A module providing convenience functionality for moving to/from numpy structured
arrays.

"""


import petl as etl
from petl.compat import next, string_types
from petl.util.base import iterpeek, ValuesView, Table


def guessdtype(table):
    import numpy as np
    # get numpy to infer dtype
    it = iter(table)
    hdr = next(it)
    flds = list(map(str, hdr))
    rows = tuple(it)
    dtype = np.rec.array(rows).dtype
    dtype.names = flds
    return dtype


def toarray(table, dtype=None, count=-1, sample=1000):
    """
    Convenience function to load data from the given `table` into a numpy 
    structured array. E.g.::

        >>> from petl import look
        >>> from petlx.array import toarray
        >>> look(table)
        +-----------+-------+-------+
        | 'foo'     | 'bar' | 'baz' |
        +===========+=======+=======+
        | 'apples'  | 1     | 2.5   |
        +-----------+-------+-------+
        | 'oranges' | 3     | 4.4   |
        +-----------+-------+-------+
        | 'pears'   | 7     | 0.1   |
        +-----------+-------+-------+
        
        >>> a = toarray(table)
        >>> a
        array([('apples', 1, 2.5), ('oranges', 3, 4.4), ('pears', 7, 0.1)], 
              dtype=[('foo', '|S7'), ('bar', '<i8'), ('baz', '<f8')])
        >>> a['foo']
        array(['apples', 'oranges', 'pears'], 
              dtype='|S7')
        >>> a['bar']
        array([1, 3, 7])
        >>> a['baz']
        array([ 2.5,  4.4,  0.1])
        >>> a['foo'][0]
        'apples'
        >>> a['bar'][1]
        3
        >>> a['baz'][2]
        0.10000000000000001
        
    If no datatype is specified, `sample` rows will be examined to infer an
    appropriate datatype for each field.
        
    The datatype can be specified as a string, e.g.:

        >>> a = toarray(table, dtype='a4, i2, f4')
        >>> a
        array([('appl', 1, 2.5), ('oran', 3, 4.400000095367432),
               ('pear', 7, 0.10000000149011612)], 
              dtype=[('foo', '|S4'), ('bar', '<i2'), ('baz', '<f4')])

    The datatype can also be partially specified, in which case datatypes will
    be inferred for other fields, e.g.:
    
        >>> a = toarray(table, dtype={'foo': 'a4'})
        >>> a
        array([('appl', 1, 2.5), ('oran', 3, 4.4), ('pear', 7, 0.1)], 
              dtype=[('foo', '|S4'), ('bar', '<i8'), ('baz', '<f8')])
    
    """
    
    import numpy as np
    it = iter(table)
    peek, it = iterpeek(it, sample)
    hdr = next(it)
    flds = list(map(str, hdr))

    if dtype is None:
        dtype = guessdtype(peek)

    elif isinstance(dtype, string_types):
        # insert field names from source table
        typestrings = [s.strip() for s in dtype.split(',')]
        dtype = [(f, t) for f, t in zip(flds, typestrings)]

    elif (isinstance(dtype, dict)
          and ('names' not in dtype or 'formats' not in dtype)):
        # allow for partial specification of dtype
        cols = etl.columns(peek)
        newdtype = {'names': [], 'formats': []}
        for f in flds:
            newdtype['names'].append(f)
            if f in dtype and isinstance(dtype[f], tuple):
                # assume fully specified
                newdtype['formats'].append(dtype[f][0])
            elif f not in dtype:
                # not specified at all
                a = np.array(cols[f])
                newdtype['formats'].append(a.dtype)
            else:
                # assume directly specified, just need to add offset
                newdtype['formats'].append(dtype[f])
        dtype = newdtype

    else:
        pass  # leave dtype as-is

    # numpy is fussy about having tuples, need to make sure
    it = (tuple(row) for row in it)
    sa = np.fromiter(it, dtype=dtype, count=count)

    return sa


def torecarray(*args, **kwargs):
    """
    Convenient shorthand for ``toarray(...).view(np.recarray)``.
    
    """

    import numpy as np
    return toarray(*args, **kwargs).view(np.recarray)


def fromarray(a):
    """
    Extract a table from a numpy structured array.
    
    """
    
    return ArrayView(a)


class ArrayView(Table):
    
    def __init__(self, a):
        self.a = a
        
    def __iter__(self):
        yield tuple(self.a.dtype.names)
        for row in self.a:
            yield tuple(row)


def valuestoarray(vals, dtype=None, count=-1, sample=1000):
    import numpy as np
    it = iter(vals)
    if dtype is None:
        peek, it = iterpeek(it, sample)
        dtype = np.array(peek).dtype
    a = np.fromiter(it, dtype=dtype, count=count)
    return a


# integrate extension with petl
etl.toarray = toarray
Table.toarray = toarray
etl.torecarray = torecarray
Table.torecarray = torecarray
etl.fromarray = fromarray
ValuesView.array = valuestoarray
