from petlx.xlsx import fromxlsx
import petl.fluent as etl
from petl.testutils import ieq


def test_fromxlsx():
    tbl = fromxlsx('fixture/test.xlsx', 'Sheet1')
    expect = (('foo', 'bar'),
              ('A', 1),
              ('B', 2),
              ('C', 2))
    ieq(expect, tbl)


def test_integration():
    tbl = etl.fromxlsx('fixture/test.xlsx', 'Sheet1').convert('bar', int)
    expect = (('foo', 'bar'),
              ('A', 1),
              ('B', 2),
              ('C', 2))
    ieq(expect, tbl)



