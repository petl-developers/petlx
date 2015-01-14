"""
Integration with HDF5 via PyTables.

"""

import sys
from contextlib import contextmanager


from petl.util import RowContainer, data, iterpeek


from petlx.util import UnsatisfiedDependency
from petlx.array import guessdtype


dep_message = """
The package pytables is required. Instructions for installation can be found 
at http://pytables.github.com/usersguide/installation.html or try apt-get install 
python-tables.
"""


def fromhdf5(source, where=None, name=None, condition=None, 
             condvars=None, start=None, stop=None, step=None):
    """
    Provides access to an HDF5 table. E.g.::
    
        >>> from petl import look
        >>> from petlx.hdf5 import fromhdf5
        >>> table1 = fromhdf5('test1.h5', '/testgroup', 'testtable')
        >>> look(table1)
        +-------+----------+
        | 'foo' | 'bar'    |
        +=======+==========+
        | 1     | 'asdfgh' |
        +-------+----------+
        | 2     | 'qwerty' |
        +-------+----------+
        | 3     | 'zxcvbn' |
        +-------+----------+
        
    Some alternative signatures::

        >>> # just specify path to table node
        ... table1 = fromhdf5('test1.h5', '/testgroup/testtable')
        >>> 
        >>> # use an existing tables.File object
        ... import tables
        >>> h5file = tables.open_file('test1.h5')
        >>> table1 = fromhdf5(h5file, '/testgroup/testtable')
        >>> 
        >>> # use an existing tables.Table object
        ... h5tbl = h5file.get_node('/testgroup/testtable')
        >>> table1 = fromhdf5(h5tbl)
        >>> 
        >>> # use a condition to filter data
        ... table2 = fromhdf5(h5tbl, condition="(foo < 3)")
        >>> look(table2)
        +-------+----------+
        | 'foo' | 'bar'    |
        +=======+==========+
        | 1     | 'asdfgh' |
        +-------+----------+
        | 2     | 'qwerty' |
        +-------+----------+

    .. versionadded:: 0.3
    
    """
    
    return HDF5View(source, where=where, name=name, 
                    condition=condition, condvars=condvars,
                    start=start, stop=stop, step=step)


class HDF5View(RowContainer):
    
    def __init__(self, source, where=None, name=None, condition=None,
                 condvars=None, start=None, stop=None, step=None):
        self.source = source
        self.where = where
        self.name = name
        self.condition = condition
        self.condvars = condvars
        self.start = start
        self.stop = stop
        self.step = step
        
    def __iter__(self):
        return iterhdf5(self.source, self.where, self.name, self.condition, 
                        self.condvars, self.start, self.stop, self.step)
    

@contextmanager
def _get_hdf5_table(source, where, name, mode='r'):

    try:
        import tables
    except ImportError as e:
        raise UnsatisfiedDependency(e, dep_message)

    needs_closing = False
    h5file = None

    # allow for polymorphic args
    if isinstance(source, tables.Table):

        # source is a table
        h5tbl = source

    elif isinstance(source, basestring):

        # assume source is the name of an HDF5 file, try to open it
        h5file = tables.open_file(source, mode=mode)
        needs_closing = True
        h5tbl = h5file.get_node(where, name=name)

    elif isinstance(source, tables.File):

        # source is an HDF5 file object
        h5file = source
        h5tbl = h5file.get_node(where, name=name)

    else:

        # invalid source
        raise Exception('invalid source argument, expected file name or '
                        'tables.File or tables.Table object, found: %r'
                        % source)

    yield h5tbl

    # tidy up
    if needs_closing:
        h5file.close()

    
@contextmanager
def _get_hdf5_file(source, mode='r'):

    try:
        import tables
    except ImportError as e:
        raise UnsatisfiedDependency(e, dep_message)

    needs_closing = False
    h5file = None

    # allow for polymorphic args
    if isinstance(source, basestring):

        # assume source is the name of an HDF5 file, try to open it
        h5file = tables.open_file(source, mode=mode)
        needs_closing = True

    elif isinstance(source, tables.File):

        # source is an HDF5 file object
        h5file = source

    else:

        # invalid source
        raise Exception('invalid source argument, expected file name or '
                        'tables.File object, found: %r' % source)

    yield h5file

    # tidy up
    if needs_closing:
        h5file.close()


def iterhdf5(source, where, name, condition, condvars, start, stop, step):

    with _get_hdf5_table(source, where, name) as h5tbl:

        # header row
        fields = tuple(h5tbl.colnames)
        yield fields
        
        # determine how to iterate over the table
        if condition is not None:
            it = h5tbl.where(condition, condvars=condvars, 
                             start=start, stop=stop, step=step)

        else:
            it = h5tbl.iterrows(start=start, stop=stop, step=step)

        # data rows
        for row in it:
            yield row[:]  # access row as a tuple


def fromhdf5sorted(source, where=None, name=None, sortby=None, checkCSI=False, 
                   start=None, stop=None, step=None):
    """
    Provides access to an HDF5 table, sorted by an indexed column, e.g.::
    
        >>> # set up a new hdf5 table to demonstrate with
        ... import tables
        >>> h5file = tables.open_file("test1.h5", mode="w", title="Test file")
        >>> h5file.create_group('/', 'testgroup', 'Test Group')
        /testgroup (Group) 'Test Group'
          children := []
        >>> class FooBar(tables.IsDescription):
        ...     foo = tables.Int32Col(pos=0)
        ...     bar = tables.StringCol(6, pos=2)
        ... 
        >>> h5table = h5file.create_table('/testgroup', 'testtable', FooBar, 'Test Table')
        >>> 
        >>> # load some data into the table
        ... table1 = (('foo', 'bar'),
        ...           (3, 'asdfgh'),
        ...           (2, 'qwerty'),
        ...           (1, 'zxcvbn'))
        >>> 
        >>> for row in table1[1:]:
        ...     for i, f in enumerate(table1[0]):
        ...         h5table.row[f] = row[i]
        ...     h5table.row.append()
        ... 
        >>> h5table.cols.foo.create_csindex() # CS index is required
        0
        >>> h5file.flush()
        >>> h5file.close()
        >>> 
        >>> # access the data, sorted by the indexed column
        ... from petl import look
        >>> from petlx.hdf5 import fromhdf5sorted
        >>> table2 = fromhdf5sorted('test1.h5', '/testgroup', 'testtable', sortby='foo')
        >>> look(table2)
        +-------+----------+
        | 'foo' | 'bar'    |
        +=======+==========+
        | 1     | 'zxcvbn' |
        +-------+----------+
        | 2     | 'qwerty' |
        +-------+----------+
        | 3     | 'asdfgh' |
        +-------+----------+

    .. versionadded:: 0.3
    
    """
    
    assert sortby is not None, 'no column specified to sort by'
    return HDF5SortedView(source, where=where, name=name, 
                          sortby=sortby, checkCSI=checkCSI,
                          start=start, stop=stop, step=step)


class HDF5SortedView(RowContainer):
    
    def __init__(self, source, where=None, name=None, sortby=None,
                 checkCSI=False, start=None, stop=None, step=None):
        self.source = source
        self.where = where
        self.name = name
        self.sortby = sortby
        self.checkCSI = checkCSI
        self.start = start
        self.stop = stop
        self.step = step
        
    def __iter__(self):
        return iterhdf5sorted(self.source, self.where, self.name, self.sortby,
                              self.checkCSI, self.start, self.stop, self.step)
    

def iterhdf5sorted(source, where, name, sortby, checkCSI, start, stop, step):

    with _get_hdf5_table(source, where, name) as h5tbl:

        # header row
        fields = tuple(h5tbl.colnames)
        yield fields
        
        it = h5tbl.itersorted(sortby,
                              checkCSI=checkCSI,
                              start=start,
                              stop=stop,
                              step=step)
        for row in it:
            yield row[:] # access row as a tuple
            

def tohdf5(table, source, where=None, name=None, create=False, drop=False,
           description=None, title='', filters=None, expectedrows=10000, 
           chunkshape=None, byteorder=None, createparents=False,
           sample=1000):
    """
    Write to an HDF5 table. If `create` is `False`, assumes the table
    already exists, and attempts to truncate it before loading. If `create`
    is `True`, a new table will be created, and if `drop` is True,
    any existing table will be dropped. If `description` is None,
    the datatype will be guessed. E.g.::
    
        >>> from petl import look
        >>> look(table1)
        +-------+----------+
        | 'foo' | 'bar'    |
        +=======+==========+
        | 1     | 'asdfgh' |
        +-------+----------+
        | 2     | 'qwerty' |
        +-------+----------+
        | 3     | 'zxcvbn' |
        +-------+----------+
        
        >>> from petlx.hdf5 import tohdf5, fromhdf5
        >>> tohdf5(table1, 'test1.h5', '/testgroup', 'testtable', create=True, createparents=True)
        >>> look(fromhdf5('test1.h5', '/testgroup', 'testtable'))
        +-------+----------+
        | 'foo' | 'bar'    |
        +=======+==========+
        | 1     | 'asdfgh' |
        +-------+----------+
        | 2     | 'qwerty' |
        +-------+----------+
        | 3     | 'zxcvbn' |
        +-------+----------+

    See also :func:`appendhdf5`.
    
    .. versionadded:: 0.3

    .. versionchanged:: 0.19

    The `drop` keyword argument is added, an attempt will only be made to
    drop an existing table at the given location if `drop` is True.
    
    """

    it = iter(table)
    
    if create:
        with _get_hdf5_file(source, mode='a') as h5file:

            if drop:
                h5file.remove_node(where, name)

            # determine datatype
            if description is None:
                peek, it = iterpeek(it, sample)
                # use a numpy dtype
                description = guessdtype(peek)

            # create the table
            h5file.create_table(where, name, description,
                                title=title,
                                filters=filters,
                                expectedrows=expectedrows,
                                chunkshape=chunkshape,
                                byteorder=byteorder,
                                createparents=createparents)

    with _get_hdf5_table(source, where, name, mode='a') as h5table:

        # truncate the existing table
        h5table.truncate(0)
        
        # load the data
        _insert(it, h5table)


def appendhdf5(table, source, where=None, name=None):
    """
    Like :func:`tohdf5` but don't truncate the table before loading.
    
    .. versionadded:: 0.3
    
    """

    with _get_hdf5_table(source, where, name, mode='a') as h5table:

        # load the data
        _insert(table, h5table)


def _insert(table, h5table):
    it = data(table) # don't need header
    for row in it:
        for i, f in enumerate(h5table.colnames):
            # depends on order of fields being the same in input table
            # and hd5 table, but field names don't need to match
            h5table.row[f] = row[i]
        h5table.row.append()
    h5table.flush() 
    
    
from petlx.integration import integrate
integrate(sys.modules[__name__])
