.. py:module:: petlx

petlx - Optional extensions to the petl package
===============================================

:mod:`petlx` is a collection of extensions to `petl <http://petl.readthedocs.org/>`_, 
a Python package for extracting, transforming and loading tables of data.

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

Installation
------------

This module is available from the `Python Package Index
<http://pypi.python.org/pypi/petlx>`_. On Linux distributions you
should be able to do ``easy_install petlx`` or ``pip install
petlx``. On Windows or Mac you can download manually, extract and run
``python setup.py install``.

Note that each submodule within the :mod:`petlx` package has
dependencies on one or more third party modules which will need to be
installed separately. 

Modules
-------

.. note:: The :mod:`petlx.ipython` module has been integrated into the main :mod:`petl` package. See the `petl docs <http://petl.readthedocs.org/TODO>`_ for more information.

.. toctree::
   :maxdepth: 2

   xls
   xlsx
   sql
   array
   dataframe
   hdf5
   whoosh
   interval
   tabix
   gff3
   vcf
   push

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
