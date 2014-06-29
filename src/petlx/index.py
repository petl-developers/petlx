__author__ = 'Alistair Miles <alimanfoo@googlemail.com>'


import operator


from petl.util import RowContainer
from petlx.util import UnsatisfiedDependency


dep_message = """
The package whoosh is required. Try pip install whoosh.
"""


def fromindex(indexdir, indexname=None):
    """
    TODO

    .. versionadded:: 0.16
    """

    return IndexContainer(indexdir, indexname=indexname)


class IndexContainer(RowContainer):

    def __init__(self, indexdir, indexname=None):
        self._indexdir = indexdir
        self._indexname = indexname

    def __iter__(self):
        return iterindex(self._indexdir, self._indexname)


def iterindex(indexdir, indexname):

    try:
        import whoosh
    except ImportError as e:
        raise UnsatisfiedDependency(e, dep_message)
    else:

        index = whoosh.index.open_dir(indexdir,
                                      indexname=indexname,
                                      readonly=True)

        try:
            # figure out the field names
            fields = (u'docnum',) + tuple(index.schema.stored_names())
            yield fields

            # yield all documents
            astuple = operator.itemgetter(*index.schema.stored_names())
            for (docnum, stored_fields_dict) in index.reader().iter_docs():
                yield (docnum,) + astuple(stored_fields_dict)

        finally:
            index.close()

