import inspect
import petl.fluent as fluent
import petl.interactive as interactive


def integrate(mod):
    # integrate with petl.fluent
    for n, c in mod.__dict__.items():
        if inspect.isfunction(c):
            if n.startswith('from'):
                setattr(fluent, n, fluent._wrap_function(c))
                setattr(fluent.FluentWrapper, n, staticmethod(fluent._wrap_function(c)))
            elif not n.startswith('_'):
                setattr(fluent.FluentWrapper, n, fluent._wrap_function(c)) 
      
    # integrate with petl.interactive
    for n, c in mod.__dict__.items():
        if inspect.isfunction(c):
            if n.startswith('from'):
                setattr(interactive, n, interactive._wrap_function(c))
                setattr(interactive.InteractiveWrapper, n, staticmethod(interactive._wrap_function(c)))
            elif not n.startswith('_'):
                setattr(interactive.InteractiveWrapper, n, interactive._wrap_function(c)) 

