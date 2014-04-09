"""
A module providing convenience functionality for moving to/from numpy structured
arrays.

"""


import sys
import inspect
from petl.util import RowContainer
from petlx.util import UnsatisfiedDependency


dep_message = """
The package pandas is required. Instructions for installation can be found
at http://pandas.pydata.org/pandas-docs/dev/install.html or try apt-get install
python-pandas.
"""


def todataframe(table, index=None, exclude=None, columns=None, coerce_float=False, nrows=None):
    """
    Convenience function to load data from the given `table` into a pandas DataFrame.

    .. versionadded:: 0.14

    """
    try:
        import pandas as pd
    except ImportError as e:
        raise UnsatisfiedDependency(e, dep_message)
    else:
        l = list(table)
        data = l[1:]
        if columns is None:
            columns = l[0]
        return pd.DataFrame.from_records(data, index=index, exclude=exclude,
                                         columns=columns, coerce_float=coerce_float,
                                         nrows=nrows)


# be backwards-compatible
todf = todataframe


def fromdataframe(df, include_index=False):
    """
    Extract a table from a pandas DataFrame.

    .. versionadded:: 0.14

    """

    return DataFrameContainer(df, include_index=include_index)


# be backwards-compatible
fromdf = fromdataframe


class DataFrameContainer(RowContainer):

    def __init__(self, df, include_index=False):
        assert hasattr(df, 'columns') and hasattr(df, 'iterrows') and inspect.ismethod(df.iterrows), 'bad argument, expected pandas.DataFrame, found %r' % df
        self.df = df
        self.include_index = include_index

    def __iter__(self):
        if self.include_index:
            yield ('index',) + tuple(self.df.columns)
            for i, row in self.df.iterrows():
                yield (i,) + tuple(row)
        else:
            yield tuple(self.df.columns)
            for _, row in self.df.iterrows():
                yield tuple(row)


from petlx.integration import integrate
integrate(sys.modules[__name__])
