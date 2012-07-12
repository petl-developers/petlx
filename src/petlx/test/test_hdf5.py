"""
Tests for the petlx.hdf5 module.

"""

from tables import openFile, IsDescription, Int32Col, Float32Col, \
                StringCol


from petlx.hdf5 import fromhdf5, fromhdf5sorted
from petl.testutils import ieq
from petl.transform import sort


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
    table2 = fromhdf5('test1.h5', '/testgroup/testtable')
    ieq(table1, table2)
    ieq(table1, table2)
    
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
    table2 = fromhdf5sorted(h5table, 'foo')
    ieq(sort(table1, 'foo'), table2)
    ieq(sort(table1, 'foo'), table2)

    # clean up    
    h5file.close()

