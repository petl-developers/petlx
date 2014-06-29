"""
Read and write xlsx files, using openpyxl.

"""

import os

import petl

from petlx.util import UnsatisfiedDependency


dep_message = """
The package openpyxl is required. Instructions for installation can be found at 
https://bitbucket.org/ericgazoni/openpyxl/wiki/Home or try pip install openpyxl.
"""


def fromxlsx(filename, sheet=None, range=None, **kwargs):
    """
    Extract a table from a sheet in an Excel (.xlsx) file.
    
    N.B., the sheet name is case sensitive, so watch out for, e.g., 'Sheet1'.

    .. versionchanged:: 0.15

    The ``sheet`` argument can be omitted, in which case the first sheet in the workbook is used by default.

    The ``range`` argument can be used to provide a range string specifying a range of cells to extract.

    Any other keyword arguments are passed through to :func:`openpyxl.load_workbook()`.

    """
    
    return XLSXView(filename, sheet=sheet, range=range, **kwargs)


class XLSXView(petl.util.RowContainer):
    
    def __init__(self, filename, sheet=None, range=None, **kwargs):
        self.filename = filename
        self.sheet = sheet
        self.range = range
        self.kwargs = kwargs

    def __iter__(self):
        try:
            import openpyxl
        except ImportError as e:
            raise UnsatisfiedDependency(e, dep_message)

        use_iterators = self.range is None
        wb = openpyxl.load_workbook(filename=self.filename,
                                    use_iterators=use_iterators, **self.kwargs)
        if self.sheet is None:
            ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        elif isinstance(self.sheet, int):
            ws = wb.get_sheet_by_name(wb.get_sheet_names()[self.sheet])
        else:
            ws = wb.get_sheet_by_name(str(self.sheet))

        if self.range is not None:
            return (tuple(cell.value for cell in row)
                    for row in ws.range(self.range))
        else:
            return (tuple(cell.value for cell in row)
                    for row in ws.iter_rows())


def toxlsx(tbl, filename, sheet=None, encoding='utf-8'):
    """
    Write a table to a new Excel (.xlsx) file.

    .. versionadded:: 0.15

    """

    try:
        import openpyxl
    except ImportError as e:
        raise UnsatisfiedDependency(e, dep_message)
    wb = openpyxl.Workbook(optimized_write=True, encoding=encoding)
    ws = wb.create_sheet(title=sheet)
    for row in tbl:
        ws.append(row)
    wb.save(filename)


import sys
from petlx.integration import integrate
integrate(sys.modules[__name__])

