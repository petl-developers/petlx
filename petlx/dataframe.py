"""
A module providing convenience functionality for moving to/from numpy structured
arrays.

"""


import inspect
import petl as etl
from petl.util.base import Table


def todataframe(table, index=None, exclude=None, columns=None,
                coerce_float=False, nrows=None):
    """
    Convenience function to load data from the given `table` into a pandas
    DataFrame.

    """
    import pandas as pd
    l = list(table)
    data = l[1:]
    if columns is None:
        columns = l[0]
    return pd.DataFrame.from_records(data, index=index, exclude=exclude,
                                     columns=columns, coerce_float=coerce_float,
                                     nrows=nrows)


def fromdataframe(df, include_index=False):
    """
    Extract a table from a pandas DataFrame.

    """

    return DataFrameView(df, include_index=include_index)


class DataFrameView(Table):

    def __init__(self, df, include_index=False):
        assert hasattr(df, 'columns') \
            and hasattr(df, 'iterrows') \
            and inspect.ismethod(df.iterrows), \
            'bad argument, expected pandas.DataFrame, found %r' % df
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


# integrate with petl
etl.todataframe = todataframe
Table.todataframe = todataframe
etl.todf = todataframe
Table.todf = todataframe
etl.fromdataframe = fromdataframe
etl.fromdf = fromdataframe
