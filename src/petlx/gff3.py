"""
Utilities for working with GFF3 files.

"""
from petl.io import fromtsv
from petl.transform import skipcomments, rowlenselect, convert, pushheader
from urllib import unquote_plus
from petl.util import HybridRow
from petl.base import RowContainer
from petlx.interval import facetintervallookup, intervaljoin, intervalleftjoin


def gff3_parse_attributes(attributes_string):
    """
    Parse a string of GFF3 attributes ('key=value' pairs delimited by ';') 
    and return a dictionary.
  
    .. versionadded:: 0.2
      
    """
    
    attributes = dict()
    fields = attributes_string.split(';')
    for f in fields:
        key, value = f.split('=')
        attributes[unquote_plus(key).strip()] = unquote_plus(value.strip()) 
    return attributes


def fromgff3(filename):
    """
    Extract feature rows from a GFF3 file. 
    
    .. versionadded:: 0.2

    """
    
    # parse file as tab-delimited
    t0 = fromtsv(filename)
    
    # push header
    t1 = pushheader(t0, ('seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes'))

    # skip comments
    t2 = skipcomments(t1, '#')
    
    # ignore any row not 9 values long (e.g., trailing fasta)
    t3 = rowlenselect(t2, 9)
    
    # parse attributes into a dict
    t4 = convert(t3, 'attributes', gff3_parse_attributes)
    
    # parse coordinates
    t5 = convert(t4, ('start', 'end'), int)

    return HybridRowView(t5)


# TODO move this to petl.base?
class HybridRowView(RowContainer):
    
    def __init__(self, wrapped):
        self.wrapped = wrapped
        
    def cachetag(self):
        return self.wrapped.cachetag()
    
    def __iter__(self):
        it = iter(self.wrapped)
        fields = it.next()
        yield fields
        for row in it:
            yield HybridRow(row, fields, missing=None)
            
            
def gff3lookup(features, facet='seqid'):
    """
    Build a GFF3 feature lookup based on interval trees. See also 
    :func:`petlx.interval.facetintervallookup`.
    
    .. versionadded:: 0.2
    
    """
    
    return facetintervallookup(features, key=facet, start='start', stop='end')


def gff3join(table, features, seqid='seqid', start='start', end='end', proximity=1):
    """
    Join with a table of GFF3 features. See also :func:`petlx.interval.intervaljoin`.
    
    .. versionadded:: 0.2
    
    """
    
    return intervaljoin(table, features, lstart=start, lstop=end, lfacet=seqid,
                        rstart='start', rstop='end', rfacet='seqid', 
                        proximity=proximity)

    
def gff3leftjoin(table, features, seqid='seqid', start='start', end='end', proximity=1):
    """
    Left join with a table of GFF3 features. See also :func:`petlx.interval.intervalleftjoin`.
    
    .. versionadded:: 0.2
    
    """
    
    return intervalleftjoin(table, features, lstart=start, lstop=end, lfacet=seqid,
                            rstart='start', rstop='end', rfacet='seqid', 
                            proximity=proximity)

    