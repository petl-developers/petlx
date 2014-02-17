"""
Read and write xls files, using xlrd.

"""

import os

import petl

from petlx.util import UnsatisfiedDependency


dep_message = """
The package xlrd is required. pip install xlrd.
"""


def fromxls(filename, sheetname):
    """
    Extract a table from a sheet in an Excel (.xls) file.
    
    N.B., the sheet name is case sensitive, so watch out for, e.g., 'Sheet1'.

    The package xlrd is required. Try ``pip install xlrd``.
        
    """
    
    return XLSView(filename, sheetname)

class XLSView(petl.util.RowContainer):
    
    def __init__(self, filename, sheetname='Sheet1'):
        self.filename = filename
        self.sheetname = sheetname

    def __iter__(self):
        try:
            import xlrd
        except ImportError as e:
            raise UnsatisfiedDependency(e, dep_message)

        wb = xlrd.open_workbook(filename=self.filename)
        ws = wb.sheet_by_name(self.sheetname)
        return (ws.row_values(rownum) for rownum in range(0,ws.nrows))
                

import sys
from petlx.integration import integrate
integrate(sys.modules[__name__])