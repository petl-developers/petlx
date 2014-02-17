# -*- coding: utf-8 -*-


from petlx.xls import fromxls
import petl.fluent as etl
from petl.testutils import ieq
import xlrd


def test_fromxls():
    tbl = fromxls('fixture/test.xls', 'Sheet1')
    expect = (('foo', 'bar'),
              ('A', 1),
              ('B', 2),
              ('C', 2),
              (u'é', xlrd.xldate.xldate_from_date_tuple((2012, 1, 1), 0)))
    ieq(expect, tbl)


def test_integration():
    tbl = etl.fromxls('fixture/test.xls', 'Sheet1')
    expect = (('foo', 'bar'),
              ('A', 1),
              ('B', 2),
              ('C', 2),
              (u'é', xlrd.xldate.xldate_from_date_tuple((2012, 1, 1), 0)))
    ieq(expect, tbl)


def test_fromxls_nosheet():
    tbl = fromxls('fixture/test.xls')
    expect = (('foo', 'bar'),
              ('A', 1),
              ('B', 2),
              ('C', 2),
              (u'é', xlrd.xldate.xldate_from_date_tuple((2012, 1, 1), 0)))
    ieq(expect, tbl)



