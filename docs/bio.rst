.. module:: petlx.bio

Biology
=======

GFF3
----

.. autofunction:: petlx.bio.gff3.fromgff3

Tabix (pysam)
-------------

.. note::

    The `pysam <TODO>`_ package is required, e.g.::

        $ pip install pysam

.. autofunction:: petlx.bio.tabix.fromtabix

Variant call format (PyVCF)
---------------------------

.. note::

    The `pyvcf <TODO>`_ package is required, e.g.::

        $ pip install pyvcf

.. autofunction:: petlx.bio.vcf.fromvcf
.. autofunction:: petlx.bio.vcf.vcfunpackinfo
.. autofunction:: petlx.bio.vcf.vcfmeltsamples
.. autofunction:: petlx.bio.vcf.vcfunpackcall
