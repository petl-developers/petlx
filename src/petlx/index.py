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
    Extract all documents from a Whoosh index.



    .. versionadded:: 0.16
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
        else:
            # TODO check it quacks like an index
            index = index_or_dirname
            needs_closing = False

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
    TODO

    .. versionadded:: 0.16
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
        else:
            # TODO check it quacks like an index
            index = index_or_dirname
            needs_closing = False

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
    TODO

    .. versionadded:: 0.16
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
        else:
            # TODO check it quacks like an index
            index = index_or_dirname
            needs_closing = False

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
    TODO

    .. versionadded:: 0.16
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
    TODO

    .. versionadded:: 0.16
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
        else:
            # TODO check it quacks like an index
            index = index_or_dirname
            needs_closing = False

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
            else:
                # TODO check it quacks like a whoosh query
                pass

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


from petlx.integration import integrate
integrate(sys.modules[__name__])

