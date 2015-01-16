# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division


import petl as etl
from petl.compat import text_type
from petl.util.base import Table


def fromtabix(filename, reference=None, start=None, stop=None, region=None,
              header=None):
    """
    Extract rows from a tabix indexed file, e.g.::

        >>> import petl as etl
        >>> # activate bio extensions
        ... import petlx.bio
        >>> table1 = etl.fromtabix('fixture/test.bed.gz',
        ...                        region='Pf3D7_02_v3')
        >>> table1
        +---------------+----------+----------+-----------------------------+
        | #chrom        | start    | end      | region                      |
        +===============+==========+==========+=============================+
        | 'Pf3D7_02_v3' | '0'      | '23100'  | 'SubtelomericRepeat'        |
        +---------------+----------+----------+-----------------------------+
        | 'Pf3D7_02_v3' | '23100'  | '105800' | 'SubtelomericHypervariable' |
        +---------------+----------+----------+-----------------------------+
        | 'Pf3D7_02_v3' | '105800' | '447300' | 'Core'                      |
        +---------------+----------+----------+-----------------------------+
        | 'Pf3D7_02_v3' | '447300' | '450450' | 'Centromere'                |
        +---------------+----------+----------+-----------------------------+
        | 'Pf3D7_02_v3' | '450450' | '862500' | 'Core'                      |
        +---------------+----------+----------+-----------------------------+
        ...

        >>> table2 = etl.fromtabix('fixture/test.bed.gz',
        ...                        region='Pf3D7_02_v3:110000-120000')
        >>> table2
        +---------------+----------+----------+--------+
        | #chrom        | start    | end      | region |
        +===============+==========+==========+========+
        | 'Pf3D7_02_v3' | '105800' | '447300' | 'Core' |
        +---------------+----------+----------+--------+

    """
    
    return TabixView(filename, reference, start, stop, region, header)


etl.fromtabix = fromtabix


class TabixView(Table):
    def __init__(self, filename, reference=None, start=None, stop=None,
                 region=None, header=None):
        self.filename = filename
        self.reference = reference
        self.start = start
        self.stop = stop
        self.region = region
        self.header = header
        
    def __iter__(self):
        from pysam import Tabixfile, asTuple
        f = Tabixfile(self.filename, mode='r')
        try:
            # header row
            if self.header is not None:
                yield self.header
            else:
                # assume last header line has fields
                h = list(f.header)
                if len(h) > 0:
                    header_line = text_type(h[-1], encoding='ascii')
                    yield tuple(header_line.split('\t'))

            # data rows
            for row in f.fetch(reference=self.reference, start=self.start,
                               end=self.stop, region=self.region,
                               parser=asTuple()):
                yield tuple(row)

        except:
            raise
        finally:
            f.close()
