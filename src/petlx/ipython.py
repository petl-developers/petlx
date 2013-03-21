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
    
    .. deprecated:: 0.6
    
    The :mod:`petl.interactive` module supports `_repr_html_` as of 0.13.1 so
    this function is not necessary. E.g., the following should give an HTML 
    rendering of the table inline within an iPython notebook::

        In [0]: from petl.interactive import etl
                tbl = [['foo', 'bar'], ['a', 1], ['b', 2]]
                etl(tbl)
        
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


def displayall(tbl):
    """
    Display *all rows* from a table inline within an iPython notebook. E.g.::
    
        In [0]: from petlx.ipython import displayall
                tbl = [['foo', 'bar'], ['a', 1], ['b', 2]]
                displayall(tbl)
                
    Alternatively, using the fluent style::
    
        In [0]: from petl.interactive import etl
                import petlx.ipython
                tbl = [['foo', 'bar'], ['a', 1], ['b', 2]]
                etl(tbl).displayall()
                
    .. versionadded:: 0.5  

    .. deprecated:: 0.6
    
    The :mod:`petl.interactive` module supports `_repr_html_` as of 0.13.1 so
    this function is not necessary. E.g., the following should give an HTML 
    rendering of the table inline within an iPython notebook::

        In [0]: from petl.interactive import etl
                tbl = [['foo', 'bar'], ['a', 1], ['b', 2]]
                etl(tbl)        
        
    """
    try:
        from IPython.core.display import display_html
    except ImportError as e:
        raise UnsatisfiedDependency(e, dep_message)        
    buf = StringSource()
    tohtml(tbl, buf)
    display_html(buf.getvalue(), raw=True)


import sys
from .integration import integrate
integrate(sys.modules[__name__])

