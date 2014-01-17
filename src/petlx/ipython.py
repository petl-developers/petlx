from petl import rowslice
from petlx.util import UnsatisfiedDependency
from petl.interactive import repr_html


dep_message = """
iPython is required. Instructions for installation can be found 
at http://ipython.org/install.html or try apt-get install 
ipython-notebook.
"""


def _display(tbl, sliceargs, **kwargs):
    try:
        from IPython.core.display import display_html
    except ImportError as e:
        raise UnsatisfiedDependency(e, dep_message)
    if sliceargs is not None:
        tbl = rowslice(tbl, *sliceargs)
    html = repr_html(tbl, **kwargs)
    display_html(html, raw=True)


def display(tbl, *sliceargs, **kwargs):
    """
    Display a table inline within an iPython notebook. E.g.::
    
        In [0]: from petlx.ipython import display
                tbl = [['foo', 'bar'], ['a', 1], ['b', 2]]
                display(tbl)
                
    Alternatively, using the fluent style::
    
        In [0]: import petl.interactive as etl
                import petlx.ipython
                tbl = etl.wrap([['foo', 'bar'], ['a', 1], ['b', 2]])
                tbl.display()
                
    .. versionadded:: 0.5  
    
    """
    if not sliceargs:
        sliceargs = (10,)  # so you don't accidentally crash the browser with too much data
    _display(tbl, sliceargs, **kwargs)


def displayall(tbl, **kwargs):
    """
    Display *all rows* from a table inline within an iPython notebook. E.g.::
    
        In [0]: from petlx.ipython import displayall
                tbl = [['foo', 'bar'], ['a', 1], ['b', 2]]
                displayall(tbl)
                
    Alternatively, using the fluent style::
    
        In [0]: import petl.interactive as etl
                import petlx.ipython
                tbl = etl.wrap([['foo', 'bar'], ['a', 1], ['b', 2]])
                tbl.displayall()
                
    .. versionadded:: 0.5  

    """
    _display(tbl, None, **kwargs)


import sys
from petlx.integration import integrate
integrate(sys.modules[__name__])

