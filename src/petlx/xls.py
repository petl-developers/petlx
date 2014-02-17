"""
Read and write xls files, using xlrd.

"""

import os

import petl

from petlx.util import UnsatisfiedDependency


dep_message = """
The package xlrd is required. Try pip install xlrd.
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
        try:
            import xlrd
        except ImportError as e:
            raise UnsatisfiedDependency(e, dep_message)

        wb = xlrd.open_workbook(filename=self.filename)
        if self.sheet is None:
            ws = wb.sheet_by_index(0)
        elif isinstance(self.sheet, int):
            ws = wb.sheet_by_index(self.sheet)
        else:
            ws = wb.sheet_by_name(str(self.sheet))
        return (tuple(ws.row_values(rownum)) for rownum in range(ws.nrows))
                

import sys
from petlx.integration import integrate
integrate(sys.modules[__name__])