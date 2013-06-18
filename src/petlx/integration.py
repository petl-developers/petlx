import petl.fluent as fluent
import petl.interactive as interactive


def integrate(mod):
    # integrate with petl.fluent
    for n, c in mod.__dict__.items():
        if callable(c):
            if n.startswith('from'): # avoids having to import anything other than "etl"
                setattr(fluent.FluentWrapper, n, staticmethod(fluent.wrap(c)))
            else:
                setattr(fluent.FluentWrapper, n, fluent.wrap(c)) 
      
    # integrate with petl.interactive
    for n, c in mod.__dict__.items():
        if callable(c):
            if n.startswith('from'): # avoids having to import anything other than "etl"
                setattr(interactive.InteractiveWrapper, n, staticmethod(interactive.wrap(c)))
            else:
                setattr(interactive.InteractiveWrapper, n, interactive.wrap(c)) 
          
