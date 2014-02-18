"""
Read and write xls files, using xlrd.

"""

import os
from itertools import izip_longest
import petl
from petlx.util import UnsatisfiedDependency


dep_message = """
The package xlrd is required. Try pip install xlrd.
"""


dep_message_write = """
The package xlwt is required. Try pip install xlwt.
"""


dep_message_utils = """
The package xlutils is required. Try pip install xlrd xlutils.
"""


def fromxls(filename, sheet=None):
    """
    Extract a table from a sheet in an Excel (.xls) file.
    
    N.B., the sheet name is case sensitive.

    The package xlrd is required. Try ``pip install xlrd``.
        
    """
    
    return XLSView(filename, sheet)


class XLSView(petl.util.RowContainer):
    
    def __init__(self, filename, sheet=None):
        self.filename = filename
        self.sheet = sheet

    def __iter__(self):
        # try:
        #     import xlrd
        # except ImportError as e:
        #     raise UnsatisfiedDependency(e, dep_message)
        #
        # wb = xlrd.open_workbook(filename=self.filename)
        # if self.sheet is None:
        #     ws = wb.sheet_by_index(0)
        # elif isinstance(self.sheet, int):
        #     ws = wb.sheet_by_index(self.sheet)
        # else:
        #     ws = wb.sheet_by_name(str(self.sheet))
        # return (tuple(ws.row_values(rownum)) for rownum in range(ws.nrows))

        # prefer implementation using xlutils.view as dates are automatically converted
        try:
            import xlutils.view
        except ImportError as e:
            raise UnsatisfiedDependency(e, dep_message_utils)

        wb = xlutils.view.View(self.filename)
        if self.sheet is None:
            ws = wb[0]
        else:
            ws = wb[self.sheet]
        return (tuple(row) for row in ws)


def toxls(tbl, filename, sheet, encoding='ascii', style_compression=0, styles=None):
    """
    Write a table to a new Excel (.xls) file.

    .. versionadded:: 0.15

    """

    try:
        import xlwt
    except ImportError as e:
        raise UnsatisfiedDependency(e, dep_message_write)
    wb = xlwt.Workbook(encoding=encoding, style_compression=style_compression)
    ws = wb.add_sheet(sheet)

    if styles is None:
        # simple version, don't worry about styles
        for r, row in enumerate(tbl):
            for c, label in enumerate(row):
                ws.write(r, c, label=label)
    else:
        # handle styles
        it = iter(tbl)
        fields = it.next()
        for c, label in enumerate(fields):
            ws.write(0, c, label=label)
            if label not in styles:
                styles[label] = xlwt.Style.default_style
        # convert to list for easy zipping
        styles = [styles[f] for f in fields]
        for r, row in enumerate(it):
            for c, (label, style) in enumerate(izip_longest(row, styles, fillvalue=None)):
                if style is None:
                    style = xlwt.Style.default_style
                ws.write(r+1, c, label=label, style=style)

    wb.save(filename)


import sys
from petlx.integration import integrate
integrate(sys.modules[__name__])