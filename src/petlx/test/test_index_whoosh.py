__author__ = 'Alistair Miles <alimanfoo@googlemail.com>'


import os
import datetime


from whoosh.index import create_in
from whoosh.fields import *


from petl.testutils import ieq
import petl.fluent as etl
from petlx.index import fromindex, toindex, appendindex, searchindex


dirname = os.path.join('tmp', 'whoosh')
if not os.path.exists('tmp'):
    os.mkdir('tmp')
if not os.path.exists(dirname):
    os.mkdir(dirname)


def test_fromindex_dirname():

    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)

    ix = create_in(dirname, schema)
    writer = ix.writer()
    writer.add_document(title=u"First document", path=u"/a",
                        content=u"This is the first document we've added!")
    writer.add_document(title=u"Second document", path=u"/b",
                        content=u"The second one is even more interesting!")
    writer.commit()

    # N.B., fields get sorted
    expect = ((u'path', u'title'),
              (u'/a', u'First document'),
              (u'/b', u'Second document'))
    actual = fromindex(dirname)
    ieq(expect, actual)


def test_fromindex_index():

    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)

    ix = create_in(dirname, schema)
    writer = ix.writer()
    writer.add_document(title=u"First document", path=u"/a",
                        content=u"This is the first document we've added!")
    writer.add_document(title=u"Second document", path=u"/b",
                        content=u"The second one is even more interesting!")
    writer.commit()

    # N.B., fields get sorted
    expect = ((u'path', u'title'),
              (u'/a', u'First document'),
              (u'/b', u'Second document'))
    actual = fromindex(ix)
    ieq(expect, actual)


def test_fromindex_docnum_field():

    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)

    ix = create_in(dirname, schema)
    writer = ix.writer()
    writer.add_document(title=u"First document", path=u"/a",
                        content=u"This is the first document we've added!")
    writer.add_document(title=u"Second document", path=u"/b",
                        content=u"The second one is even more interesting!")
    writer.commit()

    # N.B., fields get sorted
    expect = ((u'docnum', u'path', u'title'),
              (0, u'/a', u'First document'),
              (1, u'/b', u'Second document'))
    actual = fromindex(dirname, docnum_field='docnum')
    ieq(expect, actual)


def test_toindex_dirname():

    # name fields in ascending order as whoosh sorts fields on the way out
    tbl = (('f0', 'f1', 'f2', 'f3', 'f4'),
           (u'AAA', 12, 4.3, True, datetime.datetime.now()),
           (u'BBB', 6, 3.4, False, datetime.datetime(1900, 01, 31)),
           (u'CCC', 42, 7.8, True, datetime.datetime(2100, 12, 25)))

    schema = Schema(f0=TEXT(stored=True),
                    f1=NUMERIC(int, stored=True),
                    f2=NUMERIC(float, stored=True),
                    f3=BOOLEAN(stored=True),
                    f4=DATETIME(stored=True))

    toindex(tbl, dirname, schema=schema)

    actual = fromindex(dirname)
    ieq(tbl, actual)


def test_toindex_index():

    # name fields in ascending order as whoosh sorts fields on the way out
    tbl = (('f0', 'f1', 'f2', 'f3', 'f4'),
           (u'AAA', 12, 4.3, True, datetime.datetime.now()),
           (u'BBB', 6, 3.4, False, datetime.datetime(1900, 01, 31)),
           (u'CCC', 42, 7.8, True, datetime.datetime(2100, 12, 25)))

    schema = Schema(f0=TEXT(stored=True),
                    f1=NUMERIC(int, stored=True),
                    f2=NUMERIC(float, stored=True),
                    f3=BOOLEAN(stored=True),
                    f4=DATETIME(stored=True))
    index = create_in(dirname, schema)

    toindex(tbl, index)

    actual = fromindex(index)
    ieq(tbl, actual)


def test_appendindex_dirname():

    # name fields in ascending order as whoosh sorts fields on the way out
    tbl = (('f0', 'f1', 'f2', 'f3', 'f4'),
           (u'AAA', 12, 4.3, True, datetime.datetime.now()),
           (u'BBB', 6, 3.4, False, datetime.datetime(1900, 01, 31)),
           (u'CCC', 42, 7.8, True, datetime.datetime(2100, 12, 25)))

    schema = Schema(f0=TEXT(stored=True),
                    f1=NUMERIC(int, stored=True),
                    f2=NUMERIC(float, stored=True),
                    f3=BOOLEAN(stored=True),
                    f4=DATETIME(stored=True))

    toindex(tbl, dirname, schema=schema)
    appendindex(tbl, dirname)

    actual = fromindex(dirname)
    expect = tbl + tbl[1:]
    ieq(expect, actual)


def test_appendindex_index():

    # name fields in ascending order as whoosh sorts fields on the way out
    tbl = (('f0', 'f1', 'f2', 'f3', 'f4'),
           (u'AAA', 12, 4.3, True, datetime.datetime.now()),
           (u'BBB', 6, 3.4, False, datetime.datetime(1900, 01, 31)),
           (u'CCC', 42, 7.8, True, datetime.datetime(2100, 12, 25)))

    schema = Schema(f0=TEXT(stored=True),
                    f1=NUMERIC(int, stored=True),
                    f2=NUMERIC(float, stored=True),
                    f3=BOOLEAN(stored=True),
                    f4=DATETIME(stored=True))
    index = create_in(dirname, schema)

    toindex(tbl, index)
    appendindex(tbl, index)

    actual = fromindex(index)
    expect = tbl + tbl[1:]
    ieq(expect, actual)


def test_searchindex():

    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)

    ix = create_in(dirname, schema)
    writer = ix.writer()
    writer.add_document(title=u"Oranges", path=u"/a",
                        content=u"This is the first document we've added!")
    writer.add_document(title=u"Apples", path=u"/b",
                        content=u"The second document is even more "
                                u"interesting!")
    writer.commit()

    # N.B., fields get sorted
    expect = ((u'path', u'title'),
              (u'/a', u'Oranges'))
    # N.B., by default whoosh does not do stemming
    actual = searchindex(dirname, 'oranges')
    ieq(expect, actual)
    actual = searchindex(dirname, 'add*')
    ieq(expect, actual)

    expect = ((u'path', u'title'),
              (u'/a', u'Oranges'),
              (u'/b', u'Apples'))
    actual = searchindex(dirname, 'doc*')
    ieq(expect, actual)


# TODO test_searchindexpage
# TODO test_searchindex_multifield_query
# TODO test_searchindex_nontext_query

