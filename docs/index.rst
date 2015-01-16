.. py:module:: petlx

petlx - Extensions to the petl package
======================================

:mod:`petlx` is a collection of domain-specific and/or experimental
extensions to `petl <http://petl.readthedocs.org/>`_, a general
purpose Python package for extracting, transforming and loading tables
of data.

- Documentation: http://petlx.readthedocs.org/
- Source Code: https://github.com/alimanfoo/petlx
- Download: http://pypi.python.org/pypi/petlx
- Mailing List: http://groups.google.com/group/python-etl 

Please feel free to ask questions via the mailing list
(python-etl@googlegroups.com).

To report installation problems, bugs or any other issues please email
python-etl@googlegroups.com or `raise an issue on GitHub
<https://github.com/alimanfoo/petlx/issues/new>`_.

For an overview of all functions in the package, see the
:ref:`genindex`.


.. _installation:

Installation
------------

This package is available from the `Python Package Index
<http://pypi.python.org/pypi/petlx>`_. If you have `pip
<https://pip.pypa.io/>`_ you should be able to do::

    $ pip install petlx

You can also download manually, extract and run ``python setup.py
install``.


.. _dependencies:

Dependencies
------------

This package has no installation requirements other than the Python
core modules.

Some of the functions in this package require installation of third party
packages. This is indicated in the relevant parts of the documentation.


.. _modules:

Modules
-------

.. note::

   As of version 1.0 the modules :mod:`petlx.ipython`,
   :mod:`petlx.array`, :mod:`petlx.dataframe`, :mod:`petlx.xls`,
   :mod:`petlx.xlsx`, :mod:`petlx.hdf5`, :mod:`petlx.sql`,
   :mod:`petlx.interval`, :mod:`petlx.whoosh` have all been migrated
   to the main :mod:`petl` package . See the `petl docs
   <http://petl.readthedocs.org/>`_ for more information.

.. toctree::
   :maxdepth: 2

   bio
   push

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
