# -*- coding: utf-8 -*-


from petl.testutils import ieq
from datetime import datetime


def test_integration_fluent():
    import petl.fluent as etl
    import petlx.xlsx
    tbl = etl.fromxlsx('fixture/test.xlsx', 'Sheet1')
    expect = (('foo', 'bar'),
              ('A', 1),
              ('B', 2),
              ('C', 2),
              (u'é', datetime(2012, 1, 1)))
    ieq(expect, tbl)
    ieq(expect, tbl)


def test_integration_interactive():
    import petl.interactive as etl
    import petlx.xlsx
    tbl = etl.fromxlsx('fixture/test.xlsx', 'Sheet1')
    expect = (('foo', 'bar'),
              ('A', 1),
              ('B', 2),
              ('C', 2),
              (u'é', datetime(2012, 1, 1)))
    ieq(expect, tbl)
    ieq(expect, tbl)


