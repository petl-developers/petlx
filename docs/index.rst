.. py:module:: petlx

petlx - Extensions to the petl package
======================================

:mod:`petlx` is a collection of domain-specific and/or experimental
extensions to `petl`_, a general purpose Python package for
extracting, transforming and loading tables of data.

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

.. note:: 

    Version 1.0 is a new major release of :mod:`petlx`. The content of
    this package is significantly changed. See the :ref:`changes`
    section below for more information.

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

.. toctree::
   :maxdepth: 2

   bio
   push

.. _changes:

Changes
-------

Version 1.0
~~~~~~~~~~~

Version 1.0 is a new major release of both :mod:`petlx` and
:mod:`petl`. This package has been completely reorganised, and several
areas of functionality have been migrated to `petl`_. The major
changes are described below.

* The `petlx.xls` module has been migrated to `petl.io.xls`
* The `petlx.xlsx` module has been migrated to `petl.io.xlsx`
* The `petlx.array` module has been migrated to `petl.io.numpy`
* The `petlx.dataframe` module has been migrated to `petl.io.pandas`
* The `petlx.hdf5` module has been migrated to `petl.io.pytables`
* The `petlx.index` module has been migrated to `petl.io.whoosh`
* The `petlx.interval` module has been migrated to `petl.transform.intervals`
* The `display()` and `displayall()` functions from the `petlx.ipython` module have been migrated to `petl.util.vis`
* The `petlx.tabix` module has been renamed to `petlx.bio.tabix`
* The `petlx.gff3` module has been renamed to `petlx.bio.gff3`
* The `petlx.vcf` module has been renamed to `petlx.bio.vcf`

Please email python-etl@googlegroups.com if you have any questions.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _petl: http://petl.readthedocs.org/
