from petl import rowslice, tohtml
from petl.io import StringSource
from petlx.util import UnsatisfiedDependency


dep_message = """
iPython is required. Instructions for installation can be found 
at http://ipython.org/install.html or try apt-get install 
ipython-notebook.
"""


def display(tbl, *sliceargs):
    """
    Display a table inline within an iPython notebook. E.g.::
    
        In [0]: from petlx.ipython import display
                tbl = [['foo', 'bar'], ['a', 1], ['b', 2]]
                display(tbl)
                
    Alternatively, using the fluent style::
    
        In [0]: from petl.interactive import etl
                import petlx.ipython
                tbl = [['foo', 'bar'], ['a', 1], ['b', 2]]
                etl(tbl).display()
                
    .. versionadded:: 0.5  
        
    """
    try:
        from IPython.core.display import display_html
    except ImportError as e:
        raise UnsatisfiedDependency(e, dep_message)        
    if not sliceargs:
        sliceargs = (10,)
    tbl = rowslice(tbl, *sliceargs)
    buf = StringSource()
    tohtml(tbl, buf)
    display_html(buf.getvalue(), raw=True)


import sys
from .integration import integrate
integrate(sys.modules[__name__])

