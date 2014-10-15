# -*- coding: utf-8 -*-

from petlx.sql import make_sqlalchemy_column
from petl.testutils import eq_
from datetime import datetime, date
from sqlalchemy import Column, DateTime, Date


def test_make_datetime_column():
    sql_col = make_sqlalchemy_column([datetime(2014, 1, 1, 1, 1, 1, 1),
                                      datetime(2014, 1, 1, 1, 1, 1, 2)],
                                     'name')
    expect = Column('name', DateTime(), nullable=False)
    eq_(str(expect.type), str(sql_col.type))


def test_make_date_column():
    sql_col = make_sqlalchemy_column([date(2014, 1, 1),
                                      date(2014, 1, 2)],
                                     'name')
    expect = Column('name', Date(), nullable=False)
    eq_(str(expect.type), str(sql_col.type))

if __name__ == "__main__":
    test_make_date_column()
    test_make_datetime_column()