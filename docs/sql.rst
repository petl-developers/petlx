.. py:module:: petlx.sql

SQL (SQLAlchemy)
================

Extension module providing some convenience functions for working with SQL databases. SQLAlchemy is required, try
``apt-get install python-sqlalchemy`` or ``pip install SQLAlchemy``.

Acknowledgments: much of the code of this module is based on the ``csvsql`` utility in the
`csvkit <https://github.com/onyxfish/csvkit>`_ package.

.. autofunction:: petlx.sql.todb
.. autofunction:: petlx.sql.create_table
.. autofunction:: petlx.sql.drop_table
.. autofunction:: petlx.sql.make_create_table_statement
.. autofunction:: petlx.sql.make_sqlalchemy_table
.. autofunction:: petlx.sql.make_sqlalchemy_column

