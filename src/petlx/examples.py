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
