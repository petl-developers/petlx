# -*- coding: utf-8 -*-


from petlx.xlsx import fromxlsx
import petl.fluent as etl
from petl.testutils import ieq
from datetime import datetime


def test_fromxlsx():
    tbl = fromxlsx('fixture/test.xlsx', 'Sheet1')
    expect = (('foo', 'bar'),
              ('A', 1),
              ('B', 2),
              ('C', 2),
              (u'é', datetime(2012, 1, 1)))
    ieq(expect, tbl)


def test_integration():
    tbl = etl.fromxlsx('fixture/test.xlsx', 'Sheet1')
    expect = (('foo', 'bar'),
              ('A', 1),
              ('B', 2),
              ('C', 2),
              (u'é', datetime(2012, 1, 1)))
    ieq(expect, tbl)



