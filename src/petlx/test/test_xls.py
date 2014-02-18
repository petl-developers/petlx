# -*- coding: utf-8 -*-


from petlx.xls import fromxls, toxls
import petl.fluent as etl
from petl.testutils import ieq
from datetime import datetime
import xlwt


def test_fromxls():
    tbl = fromxls('fixture/test.xls', 'Sheet1')
    expect = (('foo', 'bar'),
              ('A', 1),
              ('B', 2),
              ('C', 2),
              (u'é', datetime(2012, 1, 1)))
    ieq(expect, tbl)
    ieq(expect, tbl)


def test_integration():
    tbl = etl.fromxls('fixture/test.xls', 'Sheet1')
    expect = (('foo', 'bar'),
              ('A', 1),
              ('B', 2),
              ('C', 2),
              (u'é', datetime(2012, 1, 1)))
    ieq(expect, tbl)
    ieq(expect, tbl)


def test_fromxls_nosheet():
    tbl = fromxls('fixture/test.xls')
    expect = (('foo', 'bar'),
              ('A', 1),
              ('B', 2),
              ('C', 2),
              (u'é', datetime(2012, 1, 1)))
    ieq(expect, tbl)
    ieq(expect, tbl)


def test_toxls():
    expect = (('foo', 'bar'),
              ('A', 1),
              ('B', 2),
              ('C', 2))
    toxls(expect, 'tmp/test1.xls', 'Sheet1')
    actual = fromxls('tmp/test1.xls', 'Sheet1')
    ieq(expect, actual)


def test_toxls_date():
    expect = (('foo', 'bar'),
              (u'é', datetime(2012, 1, 1)),
              (u'éé', datetime(2013, 2, 22)),
    )
    toxls(expect, 'tmp/test2.xls', 'Sheet1', styles={'bar': xlwt.easyxf(num_format_str='DD/MM/YYYY')})
    actual = fromxls('tmp/test2.xls', 'Sheet1')
    ieq(expect, actual)

