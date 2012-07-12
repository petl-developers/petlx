"""
Examples.

"""

table = [('foo', 'bar', 'baz'),
         ('apples', 1, 2.5),
         ('oranges', 3, 4.4),
         ('pears', 7, .1)]

from petl import look
from petlx.array import toarray
look(table)
a = toarray(table)
a

a = toarray(table, dtype='a4, i2, f4')
a

a = toarray(table, dtype={'foo': 'a4'})
a


table = (('type', 'start', 'stop', 'value'),
         ('apple', 1, 4, 'foo'),
         ('apple', 3, 7, 'bar'),
         ('orange', 4, 9, 'baz'))

from petl import look
from petlx.interval import facetintervallookup
look(table)
lkp = facetintervallookup(table, key='type', startfield='start', stopfield='stop')
lkp['apple'][1:2]
lkp['apple'][2:4]
lkp['apple'][2:5]
lkp['orange'][2:5]
lkp['orange'][9:14]
lkp['orange'][19:140]
lkp['apple'][1]
lkp['apple'][2]
lkp['apple'][4]
lkp['apple'][5]
lkp['orange'][5]

table = (('type', 'start', 'stop', 'value'),
         ('apple', 1, 4, 'foo'),
         ('apple', 3, 7, 'bar'),
         ('orange', 4, 9, 'baz'))

from petl import look
from petlx.interval import facetintervallookupone
look(table)
lkp = facetintervallookupone(table, key='type', startfield='start', stopfield='stop', valuespec='value')
lkp['apple'][1:2]
lkp['apple'][2:4]
lkp['apple'][2:5]
lkp['apple'][4:5]
lkp['orange'][4:5]
lkp['apple'][5:7]
lkp['orange'][5:7]
lkp['apple'][8:9]
lkp['orange'][8:9]
lkp['orange'][9:14]
lkp['orange'][19:140]
lkp['apple'][1]
lkp['apple'][2]
lkp['apple'][4]
lkp['apple'][5]
lkp['orange'][5]
lkp['apple'][8]
lkp['orange'][8]
    
    
table = (('type', 'start', 'stop', 'value'),
         ('apple', 1, 4, 'foo'),
         ('apple', 3, 7, 'bar'),
         ('orange', 4, 9, 'baz'))

from petl import look
from petlx.interval import facetintervalrecordlookup
look(table)
lkp = facetintervalrecordlookup(table, key='type', startfield='start', stopfield='stop')
lkp['apple'][1:2]
lkp['apple'][2:4]
lkp['apple'][2:5]
lkp['orange'][2:5]
lkp['orange'][9:14]
lkp['orange'][19:140]
lkp['apple'][1]
lkp['apple'][2]
lkp['apple'][4]
lkp['apple'][5]
lkp['orange'][5]

table = (('type', 'start', 'stop', 'value'),
         ('apple', 1, 4, 'foo'),
         ('apple', 3, 7, 'bar'),
         ('orange', 4, 9, 'baz'))

from petl import look
from petlx.interval import facetintervalrecordlookupone
look(table)
lkp = facetintervalrecordlookupone(table, key='type', startfield='start', stopfield='stop')
lkp['apple'][1:2]
lkp['apple'][2:4]
lkp['apple'][2:5]
lkp['apple'][4:5]
lkp['orange'][4:5]
lkp['apple'][5:7]
lkp['orange'][5:7]
lkp['apple'][8:9]
lkp['orange'][8:9]
lkp['orange'][9:14]
lkp['orange'][19:140]
lkp['apple'][1]
lkp['apple'][2]
lkp['apple'][4]
lkp['apple'][5]
lkp['orange'][5]
lkp['apple'][8]
lkp['orange'][8]


# intervaljoin
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

from petl import look
from petlx.interval import intervaljoin
look(left)
look(right)
result = intervaljoin(left, right, lstart='begin', lstop='end', rstart='start', rstop='stop')
look(result) 


# intervaljoin with facet

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

from petl import look
from petlx.interval import intervaljoin    
look(left)
look(right)
result = intervaljoin(left, right, lstart='begin', lstop='end', rstart='start', rstop='stop', lfacet='fruit', rfacet='type')
look(result)
   
   
# intervalleftjoin

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

from petl import look
from petlx.interval import intervalleftjoin
look(left)
look(right)
result = intervalleftjoin(left, right, lstart='begin', lstop='end', rstart='start', rstop='stop')
look(result)


# fromhdf5
# set up a new hdf5 table to work with
import tables
h5file = tables.openFile("test1.h5", mode="w", title="Test file")
h5file.createGroup('/', 'testgroup', 'Test Group')
class FooBar(tables.IsDescription):
    foo = tables.Int32Col(pos=0)
    bar = tables.StringCol(6, pos=2)

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

from petl import look
from petlx.hdf5 import fromhdf5
table1 = fromhdf5('test1.h5', '/testgroup', 'testtable')
look(table1)

# just specify path to table node
table1 = fromhdf5('test1.h5', '/testgroup/testtable')

# use an existing tables.File object
import tables
h5file = tables.openFile('test1.h5')
table1 = fromhdf5(h5file, '/testgroup/testtable')

# use an existing tables.Table object
h5tbl = h5file.getNode('/testgroup/testtable')
table1 = fromhdf5(h5tbl)

# use a condition to filter data
table2 = fromhdf5(h5tbl, condition="(foo < 3)")
look(table2)


# fromhdf5sorted

# set up a new hdf5 table to demonstrate with
import tables
h5file = tables.openFile("test1.h5", mode="w", title="Test file")
h5file.createGroup('/', 'testgroup', 'Test Group')
class FooBar(tables.IsDescription):
    foo = tables.Int32Col(pos=0)
    bar = tables.StringCol(6, pos=2)

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

h5table.cols.foo.createCSIndex() # CS index is required
h5file.flush()
h5file.close()

# access the data, sorted by the indexed column
from petl import look
from petlx.hdf5 import fromhdf5sorted
table2 = fromhdf5sorted('test1.h5', '/testgroup', 'testtable', sortby='foo')
look(table2)


# tohdf5
table1 = (('foo', 'bar'),
          (1, 'asdfgh'),
          (2, 'qwerty'),
          (3, 'zxcvbn'))

from petl import look
look(table1)
from petlx.hdf5 import tohdf5, fromhdf5
tohdf5(table1, 'test1.h5', '/testgroup', 'testtable', create=True, createparents=True)
look(fromhdf5('test1.h5', '/testgroup', 'testtable'))

