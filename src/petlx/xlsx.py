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


def fromxlsx(filename, sheetname):
    """
    Extract a table from a sheet in an Excel (.xlsx) file.
    
    N.B., the sheet name is case sensitive, so watch out for, e.g., 'Sheet1'.

    The package openpyxl is required. Instructions for installation can be found at 
    https://bitbucket.org/ericgazoni/openpyxl/wiki/Home or try ``pip install openpyxl``.
        
    """
    
    return XLSXView(filename, sheetname)


class XLSXView(petl.util.RowContainer):
    
    def __init__(self, filename, sheetname='Sheet1'):
        self.filename = filename
        self.sheetname = sheetname

    def __iter__(self):
        try:
            import openpyxl
        except ImportError as e:
            raise UnsatisfiedDependency(e, dep_message)
        wb = openpyxl.reader.excel.load_workbook(filename=self.filename, use_iterators=True)
        ws = wb.get_sheet_by_name(name=self.sheetname)
        return (tuple(cell.internal_value for cell in row) for row in ws.iter_rows())
                

import sys
from petlx.integration import integrate
integrate(sys.modules[__name__])

