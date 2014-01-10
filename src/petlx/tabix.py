from petl.util import RowContainer
from petlx.util import UnsatisfiedDependency


dep_message = """
The package pysam is required. Instructions for installation can be found 
at https://code.google.com/p/pysam/ or try pip install pysam.
"""


def fromtabix(filename, reference=None, start=None, end=None, region=None, header=None):
    """
    Extract rows from a tabix indexed file. E.g.::
    
        >>> from petlx.tabix import fromtabix
        >>> from petl import look
        >>> t = fromtabix('test.bed.gz', region='Pf3D7_02_v3:100000-200000')
        >>> look(t)
        +---------------+----------+----------+-----------------------------+
        | '#chrom'      | 'start'  | 'end'    | 'region'                    |
        +===============+==========+==========+=============================+
        | 'Pf3D7_02_v3' | '23100'  | '105800' | 'SubtelomericHypervariable' |
        +---------------+----------+----------+-----------------------------+
        | 'Pf3D7_02_v3' | '105800' | '447300' | 'Core'                      |
        +---------------+----------+----------+-----------------------------+
    
    .. versionadded:: 0.4
    
    """
    
    return TabixContainer(filename, reference, start, end, region, header)


class TabixContainer(RowContainer):
    
    def __init__(self, filename, reference=None, start=None, end=None, region=None, header=None):
        self.filename = filename
        self.reference = reference
        self.start = start
        self.end = end
        self.region = region
        self.header = header
        
    def __iter__(self):
        try:
            from pysam import Tabixfile, asTuple
        except ImportError as e:
            raise UnsatisfiedDependency(e, dep_message)
        f = Tabixfile(self.filename, mode='r')
        try:
            # header row
            if self.header is not None:
                yield self.header
            else:
                # assume last header line has fields
                h = list(f.header)
                if len(h) > 0:
                    yield tuple(h[-1].split('\t'))
            # data rows
            for row in f.fetch(reference=self.reference, start=self.start, end=self.end, region=self.region, parser=asTuple()):
                yield tuple(row)
        except:
            raise
        finally:
            f.close()


import sys    
from petlx.integration import integrate
integrate(sys.modules[__name__])

