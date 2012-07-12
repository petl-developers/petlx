"""
TODO doc me

"""

import tables


from petl.io import Uncacheable
from petl.util import RowContainer, HybridRow


def fromhdf5(source, where=None, name=None, condition=None, 
             condvars=None, start=None, stop=None, step=None):
    """
    TODO doc me
    
    """
    
    return HDF5View(source, where=where, name=name, 
                    condition=condition, condvars=condvars,
                    start=start, stop=stop, step=step)


class HDF5View(RowContainer):
    
    def __init__(self, source, where=None, name=None, condition=None,
                 condvars=None, start=None, stop=None, step=None):
        self.source = source
        self.where = where
        self.name = name
        self.condition = condition
        self.condvars = condvars
        self.start = start
        self.stop = stop
        self.step = step
        
    def __iter__(self):
        return iterhdf5(self.source, self.where, self.name, self.condition, 
                        self.condvars, self.start, self.stop, self.step)
    
    def cachetag(self):
        # TODO
        raise Uncacheable()
    
    
def iterhdf5(source, where, name, condition, condvars, start, stop, step):

    if isinstance(source, tables.Table):
        h5tbl = source
    else:
        if isinstance(source, basestring):
            # assume it's the name of an HDF5 file
            h5file = tables.openFile(source, mode='r')
        elif isinstance(source, tables.File):
            h5file = source
        else:
            raise Exception('invalid source argument, expected file name or tables.File or tables.Table object, found: %r' % source)
        h5tbl = h5file.getNode(where, name=name)
        assert isinstance(h5tbl, tables.Table), 'node is not a table: %r' % h5tbl
    
    try:
        fields = tuple(h5tbl.colnames)
        yield fields # header row
        
        # determine how to access the table
        if condition is not None:
            it = h5tbl.where(condition, condvars=condvars, 
                             start=start, stop=stop, step=step)
        else:
            it = h5tbl.iterrows(start=start, stop=stop, step=step)
        
        for row in it:
            yield row[:] # access row as a tuple
            
    finally:
        if isinstance(source, basestring):
            # close the file if we opened it here
            h5file.close()


def fromhdf5sorted():
    pass