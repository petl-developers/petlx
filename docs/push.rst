.. module:: petlx.push

Branching Pipelines
===================

Introduction
------------

This module provides some functions for setting up branching data
transformation pipelines.

The general pattern is to define the pipeline, connecting components
together via the ``pipe()`` method call, then pushing data through the
pipeline via the ``push()`` method call at the top of the
pipeline. E.g.::

    >>> from petl import fromcsv
    >>> source = fromcsv('fruit.csv')
    >>> from petlx.push import *
    >>> p = partition('fruit')
    >>> p.pipe('orange', tocsv('oranges.csv'))
    >>> p.pipe('banana', tocsv('bananas.csv'))
    >>> p.push(source)

The pipe operator can also be used to connect components in the
pipeline, by analogy with the use of the pipe character in unix/linux
shells, e.g.::

    >>> from petl import fromcsv
    >>> source = fromcsv('fruit.csv')
    >>> from petlx.push import *
    >>> p = partition('fruit')
    >>> p | ('orange', tocsv('oranges.csv')
    >>> p | ('banana', tocsv('bananas.csv')
    >>> p.push(source)

Push Functions
--------------

.. autofunction:: petlx.push.partition
.. autofunction:: petlx.push.sort
.. autofunction:: petlx.push.duplicates
.. autofunction:: petlx.push.unique
.. autofunction:: petlx.push.diff
.. autofunction:: petlx.push.tocsv
.. autofunction:: petlx.push.totsv
.. autofunction:: petlx.push.topickle
