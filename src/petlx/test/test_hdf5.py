"""
Tests for the petlx.hdf5 module.

"""

from itertools import chain


from tables import openFile, IsDescription, Int32Col, Float32Col, \
                StringCol
from petl.testutils import ieq
from petl.transform import sort


from petlx.hdf5 import fromhdf5, fromhdf5sorted, tohdf5, appendhdf5


def test_fromhdf5():
    
    # set up a new hdf5 table to work with
    h5file = openFile("test1.h5", mode="w", title="Test file")
    h5file.createGroup('/', 'testgroup', 'Test Group')
    class FooBar(IsDescription):
        foo = Int32Col(pos=0)
        bar = StringCol(6, pos=2)
    h5table = h5file.createTable('/testgroup', 'testtable', FooBar, 'Test Table')
    
    # load some data into the table
    table1 = (('foo', 'bar'),
              (1, 'asdfgh'),
              (2, 'qwerty'),
              (3, 'zxcvbn'))
    for row in table1[1:]:
        for i, f in enumerate(table1[0]):
            h5table.row[f] = row[i]
        h5table.row.append()
    h5file.flush()
    h5file.close()
    
    # verify we can get the data back out
    table2a = fromhdf5('test1.h5', '/testgroup', 'testtable')
    ieq(table1, table2a)
    ieq(table1, table2a)
    
    # verify we can get the data back out
    table2b = fromhdf5('test1.h5', '/testgroup/testtable')
    ieq(table1, table2b)
    ieq(table1, table2b)
    
    # verify using an existing tables.File object
    h5file = openFile('test1.h5')
    table3 = fromhdf5(h5file, '/testgroup/testtable')
    ieq(table1, table3)
    
    # verify using an existing tables.Table object
    h5tbl = h5file.getNode('/testgroup/testtable')
    table4 = fromhdf5(h5tbl)
    ieq(table1, table4)

    # verify using a condition to filter data
    table5 = fromhdf5(h5tbl, condition="(foo < 3)")
    ieq(table1[:3], table5)
    
    # clean up
    h5file.close()


def test_fromhdf5sorted():
    
    # set up a new hdf5 table to work with
    h5file = openFile("test1.h5", mode="w", title="Test file")
    h5file.createGroup('/', 'testgroup', 'Test Group')
    class FooBar(IsDescription):
        foo = Int32Col(pos=0)
        bar = StringCol(6, pos=2)
    h5table = h5file.createTable('/testgroup', 'testtable', FooBar, 'Test Table')
    
    # load some data into the table
    table1 = (('foo', 'bar'),
              (3, 'asdfgh'),
              (2, 'qwerty'),
              (1, 'zxcvbn'))
    for row in table1[1:]:
        for i, f in enumerate(table1[0]):
            h5table.row[f] = row[i]
        h5table.row.append()
    h5table.cols.foo.createCSIndex()
    h5file.flush()
    
    # verify we can get the data back out
    table2 = fromhdf5sorted(h5table, sortby='foo')
    ieq(sort(table1, 'foo'), table2)
    ieq(sort(table1, 'foo'), table2)

    # clean up    
    h5file.close()
    
    
def test_tohdf5():
    
    # set up a new hdf5 table to work with
    h5file = openFile("test2.h5", mode="w", title="Test file")
    h5file.createGroup('/', 'testgroup', 'Test Group')
    class FooBar(IsDescription):
        foo = Int32Col(pos=0)
        bar = StringCol(6, pos=2)
    h5file.createTable('/testgroup', 'testtable', FooBar, 'Test Table')
    h5file.flush()
    h5file.close()
    
    # load some data via tohdf5
    table1 = (('foo', 'bar'),
              (1, 'asdfgh'),
              (2, 'qwerty'),
              (3, 'zxcvbn'))
    
    tohdf5(table1, 'test2.h5', '/testgroup', 'testtable')
    ieq(table1, fromhdf5('test2.h5', '/testgroup', 'testtable'))

    tohdf5(table1, 'test2.h5', '/testgroup/testtable')
    ieq(table1, fromhdf5('test2.h5', '/testgroup/testtable'))

    h5file = openFile("test2.h5", mode="a")
    tohdf5(table1, h5file, '/testgroup/testtable')
    ieq(table1, fromhdf5(h5file, '/testgroup/testtable'))
    
    h5table = h5file.getNode('/testgroup/testtable')
    tohdf5(table1, h5table)
    ieq(table1, fromhdf5(h5table))
    
    # clean up
    h5file.close()
    
    
def test_tohdf5_create():
    
    
    class FooBar(IsDescription):
        foo = Int32Col(pos=0)
        bar = StringCol(6, pos=2)
    
    table1 = (('foo', 'bar'),
              (1, 'asdfgh'),
              (2, 'qwerty'),
              (3, 'zxcvbn'))

    # test creation with defined datatype
    tohdf5(table1, 'test3.h5', '/testgroup', 'testtable', create=True,
           description=FooBar, createparents=True)
    ieq(table1, fromhdf5('test3.h5', '/testgroup', 'testtable'))
    
    # test dynamically determined datatype
    tohdf5(table1, 'test3.h5', '/testgroup', 'testtable2', create=True,
           createparents=True)
    ieq(table1, fromhdf5('test3.h5', '/testgroup', 'testtable2'))
    

def test_appendhdf5():
    
    # set up a new hdf5 table to work with
    h5file = openFile("test4.h5", mode="w", title="Test file")
    h5file.createGroup('/', 'testgroup', 'Test Group')
    class FooBar(IsDescription):
        foo = Int32Col(pos=0)
        bar = StringCol(6, pos=2)
    h5file.createTable('/testgroup', 'testtable', FooBar, 'Test Table')
    h5file.flush()
    h5file.close()
    
    # load some initial data via tohdf5()
    table1 = (('foo', 'bar'),
              (1, 'asdfgh'),
              (2, 'qwerty'),
              (3, 'zxcvbn'))
    tohdf5(table1, 'test4.h5', '/testgroup', 'testtable')
    ieq(table1, fromhdf5('test4.h5', '/testgroup', 'testtable'))

    # append some more data
    appendhdf5(table1, 'test4.h5', '/testgroup', 'testtable')
    ieq(chain(table1, table1[1:]), fromhdf5('test4.h5', '/testgroup', 'testtable'))
    
    
    
    
