# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division


import petl as etl
from petl.util.base import Table


def fromvcf(filename, chrom=None, start=None, stop=None, samples=True):
    """
    Returns a table providing access to data from a variant call file (VCF).
    E.g.::

        >>> import petl as etl
        >>> # activate bio extensions
        ... import petlx.bio
        >>> table1 = etl.fromvcf('fixture/sample.vcf')
        >>> table1.look(truncate=20)
        +-------+---------+-------------+-----+--------+------+---------+----------------------+----------------------+----------------------+----------------------+
        | CHROM | POS     | ID          | REF | ALT    | QUAL | FILTER  | INFO                 | NA00001              | NA00002              | NA00003              |
        +=======+=========+=============+=====+========+======+=========+======================+======================+======================+======================+
        | '19'  |     111 | None        | 'A' | [C]    |  9.6 | None    | {}                   | Call(sample=NA00001, | Call(sample=NA00002, | Call(sample=NA00003, |
        +-------+---------+-------------+-----+--------+------+---------+----------------------+----------------------+----------------------+----------------------+
        | '19'  |     112 | None        | 'A' | [G]    |   10 | None    | {}                   | Call(sample=NA00001, | Call(sample=NA00002, | Call(sample=NA00003, |
        +-------+---------+-------------+-----+--------+------+---------+----------------------+----------------------+----------------------+----------------------+
        | '20'  |   14370 | 'rs6054257' | 'G' | [A]    |   29 | []      | {'DP': 14, 'H2': Tru | Call(sample=NA00001, | Call(sample=NA00002, | Call(sample=NA00003, |
        +-------+---------+-------------+-----+--------+------+---------+----------------------+----------------------+----------------------+----------------------+
        | '20'  |   17330 | None        | 'T' | [A]    |    3 | ['q10'] | {'DP': 11, 'NS': 3,  | Call(sample=NA00001, | Call(sample=NA00002, | Call(sample=NA00003, |
        +-------+---------+-------------+-----+--------+------+---------+----------------------+----------------------+----------------------+----------------------+
        | '20'  | 1110696 | 'rs6040355' | 'A' | [G, T] |   67 | []      | {'DP': 10, 'AA': 'T' | Call(sample=NA00001, | Call(sample=NA00002, | Call(sample=NA00003, |
        +-------+---------+-------------+-----+--------+------+---------+----------------------+----------------------+----------------------+----------------------+
        ...

    """

    return VCFView(filename, chrom=chrom, start=start, stop=stop,
                   samples=samples)


etl.fromvcf = fromvcf


VCF_HEADER = ('CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO')


class VCFView(Table):
    def __init__(self, filename, chrom=None, start=None, stop=None,
                 samples=True):
        self.filename = filename
        self.chrom = chrom
        self.start = start
        self.stop = stop
        self.samples = samples
        
    def __iter__(self):
        import vcf as pyvcf
        reader = pyvcf.Reader(filename=self.filename)
        
        # determine header
        if isinstance(self.samples, (list, tuple)):
            # specific samples requested
            yield VCF_HEADER + tuple(self.samples)
        elif self.samples:
            # all samples
            yield VCF_HEADER + tuple(reader.samples)
        else:
            # no samples
            yield VCF_HEADER
            
        # fetch region?
        if None not in [self.chrom, self.start]:
            it = reader.fetch(self.chrom, self.start, self.end)
        else:
            it = reader
            
        # yield data
        for variant in it:
            out = tuple(getattr(variant, f) for f in VCF_HEADER)
            if isinstance(self.samples, (list, tuple)):
                # specific samples requested
                out += tuple(variant.genotype(s) for s in self.samples)
            elif self.samples:
                # all samples
                out += tuple(variant.samples)
            yield out
            

def vcfunpackinfo(table, *keys):
    """
    Unpack the INFO field into separate fields. E.g.::

        >>> import petl as etl
        >>> # activate bio extensions
        ... import petlx.bio
        >>> table1 = (
        ...     etl
        ...     .fromvcf('fixture/sample.vcf', samples=None)
        ...     .vcfunpackinfo()
        ... )
        >>> table1
        +-------+---------+-------------+-----+--------+------+---------+------+------+----------------+------+------+------+------+------+
        | CHROM | POS     | ID          | REF | ALT    | QUAL | FILTER  | AA   | AC   | AF             | AN   | DB   | DP   | H2   | NS   |
        +=======+=========+=============+=====+========+======+=========+======+======+================+======+======+======+======+======+
        | '19'  |     111 | None        | 'A' | [C]    |  9.6 | None    | None | None | None           | None | None | None | None | None |
        +-------+---------+-------------+-----+--------+------+---------+------+------+----------------+------+------+------+------+------+
        | '19'  |     112 | None        | 'A' | [G]    |   10 | None    | None | None | None           | None | None | None | None | None |
        +-------+---------+-------------+-----+--------+------+---------+------+------+----------------+------+------+------+------+------+
        | '20'  |   14370 | 'rs6054257' | 'G' | [A]    |   29 | []      | None | None | [0.5]          | None | True |   14 | True |    3 |
        +-------+---------+-------------+-----+--------+------+---------+------+------+----------------+------+------+------+------+------+
        | '20'  |   17330 | None        | 'T' | [A]    |    3 | ['q10'] | None | None | [0.017]        | None | None |   11 | None |    3 |
        +-------+---------+-------------+-----+--------+------+---------+------+------+----------------+------+------+------+------+------+
        | '20'  | 1110696 | 'rs6040355' | 'A' | [G, T] |   67 | []      | 'T'  | None | [0.333, 0.667] | None | True |   10 | None |    2 |
        +-------+---------+-------------+-----+--------+------+---------+------+------+----------------+------+------+------+------+------+
        ...

    """

    result = etl.unpackdict(table, 'INFO', keys=keys)
    return result


etl.vcfunpackinfo = vcfunpackinfo
Table.vcfunpackinfo = vcfunpackinfo

    
def vcfmeltsamples(table, *samples):
    """
    Melt the samples columns. E.g.::
    
        >>> import petl as etl
        >>> # activate bio extensions
        ... import petlx.bio
        >>> table1 = (
        ...     etl
        ...     .fromvcf('fixture/sample.vcf')
        ...     .vcfmeltsamples()
        ... )
        >>> table1
        +-------+-----+------+-----+-----+------+--------+------+-----------+-----------------------------------------------------+
        | CHROM | POS | ID   | REF | ALT | QUAL | FILTER | INFO | SAMPLE    | CALL                                                |
        +=======+=====+======+=====+=====+======+========+======+===========+=====================================================+
        | '19'  | 111 | None | 'A' | [C] |  9.6 | None   | {}   | 'NA00001' | Call(sample=NA00001, CallData(GT=0|0, HQ=[10, 10])) |
        +-------+-----+------+-----+-----+------+--------+------+-----------+-----------------------------------------------------+
        | '19'  | 111 | None | 'A' | [C] |  9.6 | None   | {}   | 'NA00002' | Call(sample=NA00002, CallData(GT=0|0, HQ=[10, 10])) |
        +-------+-----+------+-----+-----+------+--------+------+-----------+-----------------------------------------------------+
        | '19'  | 111 | None | 'A' | [C] |  9.6 | None   | {}   | 'NA00003' | Call(sample=NA00003, CallData(GT=0/1, HQ=[3, 3]))   |
        +-------+-----+------+-----+-----+------+--------+------+-----------+-----------------------------------------------------+
        | '19'  | 112 | None | 'A' | [G] |   10 | None   | {}   | 'NA00001' | Call(sample=NA00001, CallData(GT=0|0, HQ=[10, 10])) |
        +-------+-----+------+-----+-----+------+--------+------+-----------+-----------------------------------------------------+
        | '19'  | 112 | None | 'A' | [G] |   10 | None   | {}   | 'NA00002' | Call(sample=NA00002, CallData(GT=0|0, HQ=[10, 10])) |
        +-------+-----+------+-----+-----+------+--------+------+-----------+-----------------------------------------------------+
        ...

    """

    result = etl.melt(table, key=VCF_HEADER, variables=samples,
                      variablefield='SAMPLE', valuefield='CALL')
    return result


etl.vcfmeltsamples = vcfmeltsamples
Table.vcfmeltsamples = vcfmeltsamples

          
def vcfunpackcall(table, *keys):
    """
    Unpack the call column. E.g.::
    
        >>> import petl as etl
        >>> # activate bio extensions
        ... import petlx.bio
        >>> table1 = (
        ...     etl
        ...     .fromvcf('fixture/sample.vcf')
        ...     .vcfmeltsamples()
        ...     .vcfunpackcall()
        ... )
        >>> table1
        +-------+-----+------+-----+-----+------+--------+------+-----------+------+------+-------+----------+
        | CHROM | POS | ID   | REF | ALT | QUAL | FILTER | INFO | SAMPLE    | DP   | GQ   | GT    | HQ       |
        +=======+=====+======+=====+=====+======+========+======+===========+======+======+=======+==========+
        | '19'  | 111 | None | 'A' | [C] |  9.6 | None   | {}   | 'NA00001' | None | None | '0|0' | [10, 10] |
        +-------+-----+------+-----+-----+------+--------+------+-----------+------+------+-------+----------+
        | '19'  | 111 | None | 'A' | [C] |  9.6 | None   | {}   | 'NA00002' | None | None | '0|0' | [10, 10] |
        +-------+-----+------+-----+-----+------+--------+------+-----------+------+------+-------+----------+
        | '19'  | 111 | None | 'A' | [C] |  9.6 | None   | {}   | 'NA00003' | None | None | '0/1' | [3, 3]   |
        +-------+-----+------+-----+-----+------+--------+------+-----------+------+------+-------+----------+
        | '19'  | 112 | None | 'A' | [G] |   10 | None   | {}   | 'NA00001' | None | None | '0|0' | [10, 10] |
        +-------+-----+------+-----+-----+------+--------+------+-----------+------+------+-------+----------+
        | '19'  | 112 | None | 'A' | [G] |   10 | None   | {}   | 'NA00002' | None | None | '0|0' | [10, 10] |
        +-------+-----+------+-----+-----+------+--------+------+-----------+------+------+-------+----------+
        ...

    """

    result = (
        etl.wrap(table)
        .convert('CALL', lambda v: v.data._asdict())
        .unpackdict('CALL', keys=keys)
    )
    return result


etl.vcfunpackcall = vcfunpackcall
Table.vcfunpackcall = vcfunpackcall
