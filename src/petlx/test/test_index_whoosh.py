__author__ = 'Alistair Miles <alimanfoo@googlemail.com>'


import os


from whoosh.index import create_in
from whoosh.fields import *


from petl.testutils import ieq
import petl.fluent as etl
from petlx.index import fromindex


def test_fromindex():

    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)

    indexdir = os.path.join('tmp', 'whoosh')
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)

    ix = create_in(indexdir, schema)
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
    actual = fromindex(indexdir)
    ieq(expect, actual)
