##########################
# Whoosh index integration
##########################


# fromindex
###########

# set up an index and load some documents via the Whoosh API
from whoosh.index import create_in
from whoosh.fields import *
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
index = create_in('tmp/example', schema)
writer = index.writer()
writer.add_document(title=u"First document", path=u"/a",
                    content=u"This is the first document we've added!")
writer.add_document(title=u"Second document", path=u"/b",
                    content=u"The second one is even more interesting!")
writer.commit()
# extract documents as a table
from petl import look
from petlx.index import fromindex
tbl = fromindex('tmp/example')
look(tbl)


# toindex
#########

import datetime
tbl = (('f0', 'f1', 'f2', 'f3', 'f4'),
       (u'AAA', 12, 4.3, True, datetime.datetime.now()),
       (u'BBB', 6, 3.4, False, datetime.datetime(1900, 01, 31)),
       (u'CCC', 42, 7.8, True, datetime.datetime(2100, 12, 25)))

from petl import look
from petlx.index import toindex, fromindex
# here is the table we want to load into an index
look(tbl)
# define a schema for the index
from whoosh.fields import *
schema = Schema(f0=TEXT(stored=True),
                f1=NUMERIC(int, stored=True),
                f2=NUMERIC(float, stored=True),
                f3=BOOLEAN(stored=True),
                f4=DATETIME(stored=True))
# load data
toindex(tbl, 'tmp/example', schema=schema)
# look what it did
look(fromindex('tmp/example'))


# searchindex
#############


# set up an index and load some documents via the Whoosh API
from whoosh.index import create_in
from whoosh.fields import *
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
index = create_in('tmp/example', schema)
writer = index.writer()
writer.add_document(title=u"Oranges", path=u"/a",
                    content=u"This is the first document we've added!")
writer.add_document(title=u"Apples", path=u"/b",
                    content=u"The second document is even more "
                            u"interesting!")
writer.commit()
# demonstrate the use of searchindex()
from petl import look
from petlx.index import searchindex
look(searchindex('tmp/example', 'oranges'))
look(searchindex('tmp/example', 'doc*'))

