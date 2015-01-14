# -*- coding: utf-8 -*-


from petlx.xlsx import fromxlsx, toxlsx
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
    ieq(expect, tbl)


def test_fromxlsx_nosheet():
    tbl = fromxlsx('fixture/test.xlsx')
    expect = (('foo', 'bar'),
              ('A', 1),
              ('B', 2),
              ('C', 2),
              (u'é', datetime(2012, 1, 1)))
    ieq(expect, tbl)
    ieq(expect, tbl)


def test_fromxlsx_range():
    tbl = fromxlsx('fixture/test.xlsx', 'Sheet2', range_string='B2:C6')
    expect = (('foo', 'bar'),
              ('A', 1),
              ('B', 2),
              ('C', 2),
              (u'é', datetime(2012, 1, 1)))
    ieq(expect, tbl)
    ieq(expect, tbl)


def test_toxlsx():
    tbl = (('foo', 'bar'),
           ('A', 1),
           ('B', 2),
           ('C', 2),
           (u'é', datetime(2012, 1, 1)))
    toxlsx(tbl, 'tmp/test1.xlsx', 'Sheet1')
    actual = fromxlsx('tmp/test1.xlsx', 'Sheet1')
    ieq(tbl, actual)


def test_toxlsx_nosheet():
    tbl = (('foo', 'bar'),
           ('A', 1),
           ('B', 2),
           ('C', 2),
           (u'é', datetime(2012, 1, 1)))
    toxlsx(tbl, 'tmp/test2.xlsx')
    actual = fromxlsx('tmp/test2.xlsx')
    ieq(tbl, actual)


