"""
Read and write xlsx files, using openpyxl.

"""

import os

import petl

from petlx.util import UnsatisfiedDependency


def fromxlsx(filename, sheetname, checksumfun=None):
    """
    Extract a table from a sheet in an Excel (.xlsx) file.
    
    Note that the package openpyxl is required. Instructions for installation 
    can be found at https://bitbucket.org/ericgazoni/openpyxl/wiki/Home.
    
    N.B., the sheet name is case sensitive, so watch out for, e.g., 'Sheet1'.
    
    """
    
    return XLSXView(filename, sheetname, checksumfun=checksumfun)


class XLSXView(object):
    
    def __init__(self, filename, sheetname, checksumfun=None):
        self.filename = filename
        self.sheetname = sheetname
        self.checksumfun = checksumfun
        
    def __iter__(self):
        try:
            import openpyxl
        except ImportError as e:
            raise UnsatisfiedDependency(e, 'The package openpyxl is required. Instructions for installation can be found at https://bitbucket.org/ericgazoni/openpyxl/wiki/Home')
        else:
            wb = openpyxl.reader.excel.load_workbook(filename=self.filename, use_iterators=True)
            ws = wb.get_sheet_by_name(name=self.sheetname)
            return ([cell.internal_value for cell in row] for row in ws.iter_rows())
                
    def cachetag(self):
        p = self.filename
        if os.path.isfile(p):
            sumfun = self.checksumfun if self.checksumfun is not None else petl.io.defaultsumfun
            checksum = sumfun(p)
            return hash((checksum, self.sheetname)) 
        else:
            raise petl.io.Uncacheable
                
    

