"""
Examples.

"""





# intervaljoin with facet

left = (('fruit', 'begin', 'end'),
        ('apple', 1, 2),
        ('apple', 2, 4),
        ('apple', 2, 5),
        ('orange', 2, 5),
        ('orange', 9, 14),
        ('orange', 19, 140),
        ('apple', 1, 1))
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





