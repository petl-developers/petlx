# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division


from petl.compat import PY2
if PY2:
    from urllib import unquote_plus
else:
    from urllib.parse import unquote_plus


import petl as etl
# activate tabix extension
import petlx.bio.tabix


def gff3_parse_attributes(attributes_string):
    """
    Parse a string of GFF3 attributes ('key=value' pairs delimited by ';') 
    and return a dictionary.
  
    """
    
    attributes = dict()
    fields = attributes_string.split(';')
    for f in fields:
        if '=' in f:
            key, value = f.split('=')
            attributes[unquote_plus(key).strip()] = unquote_plus(value.strip())
        elif len(f) > 0:
            # not strictly kosher
            attributes[unquote_plus(f).strip()] = True            
    return attributes


GFF3_HEADER = ('seqid', 'source', 'type', 'start', 'end', 'score', 'strand',
               'phase', 'attributes')


def fromgff3(filename, region=None):
    """
    Extract feature rows from a GFF3 file, e.g.::

        >>> import petl as etl
        >>> # activate bio extensions
        ... import petlx.bio
        >>> table1 = etl.fromgff3('fixture/sample.gff')
        >>> table1.look(truncate=30)
        +--------------+---------+---------------+-------+---------+-------+--------+-------+--------------------------------+
        | seqid        | source  | type          | start | end     | score | strand | phase | attributes                     |
        +==============+=========+===============+=======+=========+=======+========+=======+================================+
        | 'apidb|MAL1' | 'ApiDB' | 'supercontig' |     1 |  643292 | '.'   | '+'    | '.'   | {'localization': 'nuclear', 'o |
        +--------------+---------+---------------+-------+---------+-------+--------+-------+--------------------------------+
        | 'apidb|MAL2' | 'ApiDB' | 'supercontig' |     1 |  947102 | '.'   | '+'    | '.'   | {'localization': 'nuclear', 'o |
        +--------------+---------+---------------+-------+---------+-------+--------+-------+--------------------------------+
        | 'apidb|MAL3' | 'ApiDB' | 'supercontig' |     1 | 1060087 | '.'   | '+'    | '.'   | {'localization': 'nuclear', 'o |
        +--------------+---------+---------------+-------+---------+-------+--------+-------+--------------------------------+
        | 'apidb|MAL4' | 'ApiDB' | 'supercontig' |     1 | 1204112 | '.'   | '+'    | '.'   | {'localization': 'nuclear', 'o |
        +--------------+---------+---------------+-------+---------+-------+--------+-------+--------------------------------+
        | 'apidb|MAL5' | 'ApiDB' | 'supercontig' |     1 | 1343552 | '.'   | '+'    | '.'   | {'localization': 'nuclear', 'o |
        +--------------+---------+---------------+-------+---------+-------+--------+-------+--------------------------------+
        ...

    A region query string of the form '[seqid]' or '[seqid]:[start]-[end]'
    may be given for the `region` argument. If given, requires the GFF3
    file to be position sorted, bgzipped and tabix indexed. Requires pysam to be
    installed. E.g.::

        >>> # extract from a specific genome region via tabix
        ... table2 = etl.fromgff3('fixture/sample.sorted.gff.gz',
        ...                       region='apidb|MAL5:1289593-1289595')
        >>> table2.look(truncate=30)
        +--------------+---------+---------------+---------+---------+-------+--------+-------+--------------------------------+
        | seqid        | source  | type          | start   | end     | score | strand | phase | attributes                     |
        +==============+=========+===============+=========+=========+=======+========+=======+================================+
        | 'apidb|MAL5' | 'ApiDB' | 'supercontig' |       1 | 1343552 | '.'   | '+'    | '.'   | {'localization': 'nuclear', 'o |
        +--------------+---------+---------------+---------+---------+-------+--------+-------+--------------------------------+
        | 'apidb|MAL5' | 'ApiDB' | 'exon'        | 1289594 | 1291685 | '.'   | '+'    | '.'   | {'size': '2092', 'Parent': 'ap |
        +--------------+---------+---------------+---------+---------+-------+--------+-------+--------------------------------+
        | 'apidb|MAL5' | 'ApiDB' | 'gene'        | 1289594 | 1291685 | '.'   | '+'    | '.'   | {'ID': 'apidb|MAL5_18S', 'web_ |
        +--------------+---------+---------------+---------+---------+-------+--------+-------+--------------------------------+
        | 'apidb|MAL5' | 'ApiDB' | 'rRNA'        | 1289594 | 1291685 | '.'   | '+'    | '.'   | {'ID': 'apidb|rna_MAL5_18S-1', |
        +--------------+---------+---------------+---------+---------+-------+--------+-------+--------------------------------+

    """

    if region is None:

        # parse file as tab-delimited
        table = etl.fromtsv(filename)

    else:

        # extract via tabix
        table = etl.fromtabix(filename, region=region)

    return (
        table
        .pushheader(GFF3_HEADER)
        .skipcomments('#')
        # ignore any row not 9 values long (e.g., trailing fasta)
        .rowlenselect(9)
        # parse attributes into a dict
        .convert('attributes', gff3_parse_attributes)
        # parse coordinates
        .convert(('start', 'end'), int)
    )


etl.fromgff3 = fromgff3
