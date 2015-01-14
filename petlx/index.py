__author__ = 'Alistair Miles <alimanfoo@googlemail.com>'


import operator
import itertools
import sys


from petl.util import RowContainer, dicts
from petlx.util import UnsatisfiedDependency


dep_message = """
The package whoosh is required. Try pip install whoosh.
"""


def fromindex(index_or_dirname, indexname=None, docnum_field=None):
    """
    Extract all documents from a Whoosh index. E.g.::

        >>> # set up an index and load some documents via the Whoosh API
        ... from whoosh.index import create_in
        >>> from whoosh.fields import *
        >>> schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
        >>> index = create_in('tmp/example', schema)
        >>> writer = index.writer()
        >>> writer.add_document(title=u"First document", path=u"/a",
        ...                     content=u"This is the first document we've added!")
        >>> writer.add_document(title=u"Second document", path=u"/b",
        ...                     content=u"The second one is even more interesting!")
        >>> writer.commit()
        >>> # extract documents as a table
        ... from petl import look
        >>> from petlx.index import fromindex
        >>> tbl = fromindex('tmp/example')
        >>> look(tbl)
        +--------+--------------------+
        | 'path' | 'title'            |
        +========+====================+
        | u'/a'  | u'First document'  |
        +--------+--------------------+
        | u'/b'  | u'Second document' |
        +--------+--------------------+

    .. versionadded:: 0.16

    Parameters
    ----------

    index_or_dirname
        Either an instance of `whoosh.index.Index` or a string containing the
        directory path where the index is stored.
    indexname
        String containing the name of the index, if multiple indexes are stored
        in the same directory.
    docnum_field
        If not None, an extra field will be added to the output table containing
        the internal document number stored in the index. The name of the field
        will be the value of this argument.

    Returns
    -------

        A table-like object (row container).

    """

    return IndexContainer(index_or_dirname,
                          indexname=indexname,
                          docnum_field=docnum_field)


class IndexContainer(RowContainer):

    def __init__(self, index_or_dirname, indexname=None, docnum_field=None):
        self._index_or_dirname = index_or_dirname
        self._indexname = indexname
        self._docnum_field = docnum_field

    def __iter__(self):
        return iterindex(self._index_or_dirname,
                         self._indexname,
                         self._docnum_field)


def iterindex(index_or_dirname, indexname, docnum_field):
    try:
        import whoosh
    except ImportError as e:
        raise UnsatisfiedDependency(e, dep_message)
    else:

        if isinstance(index_or_dirname, basestring):
            dirname = index_or_dirname
            index = whoosh.index.open_dir(dirname,
                                          indexname=indexname,
                                          readonly=True)
            needs_closing = True
        elif isinstance(index_or_dirname, whoosh.index.Index):
            index = index_or_dirname
            needs_closing = False
        else:
            raise Exception('expected string or index, found %r'
                            % index_or_dirname)

        try:

            if docnum_field is None:

                # figure out the field names
                fields = tuple(index.schema.stored_names())
                yield fields

                # yield all documents
                astuple = operator.itemgetter(*index.schema.stored_names())
                for _, stored_fields_dict in index.reader().iter_docs():
                    yield astuple(stored_fields_dict)

            else:

                # figure out the field names
                fields = (docnum_field,) + tuple(index.schema.stored_names())
                yield fields

                # yield all documents
                astuple = operator.itemgetter(*index.schema.stored_names())
                for docnum, stored_fields_dict in index.reader().iter_docs():
                    yield (docnum,) + astuple(stored_fields_dict)

        except:
            raise

        finally:
            if needs_closing:
                # close the index if we're the ones who opened it
                index.close()


def toindex(tbl, index_or_dirname, schema=None, indexname=None, merge=False,
            optimize=False):
    """
    Load all rows from `tbl` into a Whoosh index. N.B., this will clear any
    existing data in the index before loading. E.g.::

        >>> from petl import look
        >>> from petlx.index import toindex, fromindex
        >>> # here is the table we want to load into an index
        ... look(tbl)
        +--------+------+------+-------+--------------------------------------------------+
        | 'f0'   | 'f1' | 'f2' | 'f3'  | 'f4'                                             |
        +========+======+======+=======+==================================================+
        | u'AAA' |   12 |  4.3 | True  | datetime.datetime(2014, 6, 30, 14, 7, 2, 333199) |
        +--------+------+------+-------+--------------------------------------------------+
        | u'BBB' |    6 |  3.4 | False | datetime.datetime(1900, 1, 31, 0, 0)             |
        +--------+------+------+-------+--------------------------------------------------+
        | u'CCC' |   42 |  7.8 | True  | datetime.datetime(2100, 12, 25, 0, 0)            |
        +--------+------+------+-------+--------------------------------------------------+

        >>> # define a schema for the index
        ... from whoosh.fields import *
        >>> schema = Schema(f0=TEXT(stored=True),
        ...                 f1=NUMERIC(int, stored=True),
        ...                 f2=NUMERIC(float, stored=True),
        ...                 f3=BOOLEAN(stored=True),
        ...                 f4=DATETIME(stored=True))
        >>> # load data
        ... toindex(tbl, 'tmp/example', schema=schema)
        >>> # look what it did
        ... look(fromindex('tmp/example'))
        +--------+------+------+-------+--------------------------------------------------+
        | 'f0'   | 'f1' | 'f2' | 'f3'  | 'f4'                                             |
        +========+======+======+=======+==================================================+
        | u'AAA' |   12 |  4.3 | True  | datetime.datetime(2014, 6, 30, 14, 7, 2, 333199) |
        +--------+------+------+-------+--------------------------------------------------+
        | u'BBB' |    6 |  3.4 | False | datetime.datetime(1900, 1, 31, 0, 0)             |
        +--------+------+------+-------+--------------------------------------------------+
        | u'CCC' |   42 |  7.8 | True  | datetime.datetime(2100, 12, 25, 0, 0)            |
        +--------+------+------+-------+--------------------------------------------------+

    .. versionadded:: 0.16

    Parameters
    ----------

    tbl
        A table-like object (row container) containing the data to be loaded.
    index_or_dirname
        Either an instance of `whoosh.index.Index` or a string containing the
        directory path where the index is to be stored.
    indexname
        String containing the name of the index, if multiple indexes are stored
        in the same directory.
    merge
        Merge small segments during commit?
    optimize
        Merge all segments together?

    """
    try:
        import whoosh
    except ImportError as e:
        raise UnsatisfiedDependency(e, dep_message)
    else:

        # deal with polymorphic argument
        if isinstance(index_or_dirname, basestring):
            dirname = index_or_dirname
            index = whoosh.index.create_in(dirname, schema,
                                           indexname=indexname)
            needs_closing = True
        elif isinstance(index_or_dirname, whoosh.index.Index):
            index = index_or_dirname
            needs_closing = False
        else:
            raise Exception('expected string or index, found %r'
                            % index_or_dirname)

        writer = index.writer()
        try:

            for d in dicts(tbl):
                writer.add_document(**d)
            writer.commit(merge=merge, optimize=optimize,
                          mergetype=whoosh.writing.CLEAR)

        except:
            writer.cancel()
            raise

        finally:
            if needs_closing:
                index.close()


def appendindex(tbl, index_or_dirname, indexname=None, merge=True,
                optimize=False):
    """
    Load all rows from `tbl` into a Whoosh index, adding them to any existing
    data in the index.

    .. versionadded:: 0.16

    Parameters
    ----------

    tbl
        A table-like object (row container) containing the data to be loaded.
    index_or_dirname
        Either an instance of `whoosh.index.Index` or a string containing the
        directory path where the index is to be stored.
    indexname
        String containing the name of the index, if multiple indexes are stored
        in the same directory.
    merge
        Merge small segments during commit?
    optimize
        Merge all segments together?

    """
    try:
        import whoosh
    except ImportError as e:
        raise UnsatisfiedDependency(e, dep_message)
    else:

        # deal with polymorphic argument
        if isinstance(index_or_dirname, basestring):
            dirname = index_or_dirname
            index = whoosh.index.open_dir(dirname, indexname=indexname,
                                          readonly=False)
            needs_closing = True
        elif isinstance(index_or_dirname, whoosh.index.Index):
            index = index_or_dirname
            needs_closing = False
        else:
            raise Exception('expected string or index, found %r'
                            % index_or_dirname)

        writer = index.writer()
        try:

            for d in dicts(tbl):
                writer.add_document(**d)
            writer.commit(merge=merge, optimize=optimize)

        except Exception as e:
            writer.cancel()
            raise

        finally:
            if needs_closing:
                index.close()


def searchindex(index_or_dirname, query,
                limit=10,
                indexname=None,
                docnum_field=None,
                score_field=None,
                fieldboosts=None,
                search_kwargs=dict()):
    """
    Search an index using a query. E.g.::

        >>> # set up an index and load some documents via the Whoosh API
        ... from whoosh.index import create_in
        >>> from whoosh.fields import *
        >>> schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
        >>> index = create_in('tmp/example', schema)
        >>> writer = index.writer()
        >>> writer.add_document(title=u"Oranges", path=u"/a",
        ...                     content=u"This is the first document we've added!")
        >>> writer.add_document(title=u"Apples", path=u"/b",
        ...                     content=u"The second document is even more "
        ...                             u"interesting!")
        >>> writer.commit()
        >>> # demonstrate the use of searchindex()
        ... from petl import look
        >>> from petlx.index import searchindex
        >>> look(searchindex('tmp/example', 'oranges'))
        +--------+------------+
        | 'path' | 'title'    |
        +========+============+
        | u'/a'  | u'Oranges' |
        +--------+------------+

        >>> look(searchindex('tmp/example', 'doc*'))
        +--------+------------+
        | 'path' | 'title'    |
        +========+============+
        | u'/a'  | u'Oranges' |
        +--------+------------+
        | u'/b'  | u'Apples'  |
        +--------+------------+

    .. versionadded:: 0.16

    Parameters
    ----------

    index_or_dirname
        Either an instance of `whoosh.index.Index` or a string containing the
        directory path where the index is to be stored.
    query
        Either a string or an instance of `whoosh.query.Query`. If a string,
        it will be parsed as a multi-field query, i.e., any terms not bound
        to a specific field will match **any** field.
    limit
        Return at most `limit` results.
    indexname
        String containing the name of the index, if multiple indexes are stored
        in the same directory.
    docnum_field
        If not None, an extra field will be added to the output table containing
        the internal document number stored in the index. The name of the field
        will be the value of this argument.
    score_field
        If not None, an extra field will be added to the output table containing
        the score of the result. The name of the field will be the value of this
        argument.
    fieldboosts
        An optional dictionary mapping field names to boosts.
    search_kwargs
        Any extra keyword arguments to be passed through to the Whoosh
        `search()` method.

    Returns
    -------

    A table-like object (row container).

    """

    return SearchIndexContainer(index_or_dirname, query,
                                limit=limit,
                                indexname=indexname,
                                docnum_field=docnum_field,
                                score_field=score_field,
                                fieldboosts=fieldboosts,
                                search_kwargs=search_kwargs)


def searchindexpage(index_or_dirname, query, pagenum,
                    pagelen=10,
                    indexname=None,
                    docnum_field=None,
                    score_field=None,
                    fieldboosts=None,
                    search_kwargs=dict()):
    """
    Search an index using a query, returning a result page.

    .. versionadded:: 0.16

    Parameters
    ----------

    index_or_dirname
        Either an instance of `whoosh.index.Index` or a string containing the
        directory path where the index is to be stored.
    query
        Either a string or an instance of `whoosh.query.Query`. If a string,
        it will be parsed as a multi-field query, i.e., any terms not bound
        to a specific field will match **any** field.
    pagenum
        Number of the page to return (e.g., 1 = first page).
    pagelen
        Number of results per page.
    indexname
        String containing the name of the index, if multiple indexes are stored
        in the same directory.
    docnum_field
        If not None, an extra field will be added to the output table containing
        the internal document number stored in the index. The name of the field
        will be the value of this argument.
    score_field
        If not None, an extra field will be added to the output table containing
        the score of the result. The name of the field will be the value of this
        argument.
    fieldboosts
        An optional dictionary mapping field names to boosts.
    search_kwargs
        Any extra keyword arguments to be passed through to the Whoosh
        `search()` method.

    Returns
    -------

    A table-like object (row container).

    """

    return SearchIndexContainer(index_or_dirname, query,
                                pagenum=pagenum, pagelen=pagelen,
                                indexname=indexname,
                                docnum_field=docnum_field,
                                score_field=score_field,
                                fieldboosts=fieldboosts,
                                search_kwargs=search_kwargs)


class SearchIndexContainer(RowContainer):

    def __init__(self, index_or_dirname, query, limit=None, pagenum=None,
                 pagelen=None, indexname=None, docnum_field=None,
                 score_field=None, fieldboosts=None, search_kwargs=dict()):
        self._index_or_dirname = index_or_dirname
        self._query = query
        self._limit = limit
        self._pagenum = pagenum
        self._pagelen = pagelen
        self._indexname = indexname
        self._docnum_field = docnum_field
        self._score_field = score_field
        self._fieldboosts = fieldboosts
        self._search_kwargs = search_kwargs

    def __iter__(self):
        return itersearchindex(self._index_or_dirname, self._query,
                               self._limit, self._pagenum, self._pagelen,
                               self._indexname, self._docnum_field,
                               self._score_field, self._fieldboosts,
                               self._search_kwargs)


def itersearchindex(index_or_dirname, query, limit, pagenum, pagelen, indexname,
                    docnum_field, score_field, fieldboosts, search_kwargs):
    try:
        import whoosh
        import whoosh.qparser
    except ImportError as e:
        raise UnsatisfiedDependency(e, dep_message)
    else:

        if isinstance(index_or_dirname, basestring):
            dirname = index_or_dirname
            index = whoosh.index.open_dir(dirname,
                                          indexname=indexname,
                                          readonly=True)
            needs_closing = True
        elif isinstance(index_or_dirname, whoosh.index.Index):
            index = index_or_dirname
            needs_closing = False
        else:
            raise Exception('expected string or index, found %r'
                            % index_or_dirname)

        try:

            # figure out header
            fields = tuple()
            if docnum_field is not None:
                fields += (docnum_field,)
            if score_field is not None:
                fields += (score_field,)
            stored_names = tuple(index.schema.stored_names())
            fields += stored_names
            yield fields

            # parse the query
            if isinstance(query, basestring):
                # search all fields by default
                parser = whoosh.qparser.MultifieldParser(
                    index.schema.names(),
                    index.schema,
                    fieldboosts=fieldboosts
                )
                query = parser.parse(query)
            elif isinstance(query, whoosh.query.Query):
                pass
            else:
                raise Exception(
                    'expected string or whoosh.query.Query, found %r' % query
                )

            # make a function to turn docs into tuples
            astuple = operator.itemgetter(*index.schema.stored_names())

            with index.searcher() as searcher:
                if limit is not None:
                    results = searcher.search(query, limit=limit,
                                              **search_kwargs)
                else:
                    results = searcher.search_page(query, pagenum,
                                                   pagelen=pagelen,
                                                   **search_kwargs)

                if docnum_field is None and score_field is None:

                    for doc in results:
                        yield astuple(doc)

                else:

                    for (docnum, score), doc in itertools.izip(results.items(),
                                                               results):
                        row = tuple()
                        if docnum_field is not None:
                            row += (docnum,)
                        if score_field is not None:
                            row += (score,)
                        row += astuple(doc)
                        yield row

        except:
            raise

        finally:
            if needs_closing:
                # close the index if we're the ones who opened it
                index.close()


# TODO guess schema


from petlx.integration import integrate
integrate(sys.modules[__name__])
