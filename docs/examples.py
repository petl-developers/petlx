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


