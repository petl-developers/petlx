# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division


# fromtabix()
#############

import petl as etl
# activate bio extensions
import petlx.bio
table1 = etl.fromtabix('fixture/test.bed.gz',
                       region='Pf3D7_02_v3')
table1
table2 = etl.fromtabix('fixture/test.bed.gz',
                       region='Pf3D7_02_v3:110000-120000')
table2


# fromgff3()
############

import petl as etl
# activate bio extensions
import petlx.bio
table1 = etl.fromgff3('fixture/sample.gff')
table1.look(truncate=30)
# extract from a specific genome region via tabix
table2 = etl.fromgff3('fixture/sample.sorted.gff.gz',
                      region='apidb|MAL5:1289593-1289595')
table2.look(truncate=30)


# fromvcf()
###########

import petl as etl
# activate bio extensions
import petlx.bio
table1 = etl.fromvcf('fixture/sample.vcf')
table1.look(truncate=20)


# vcfunpackinfo()
#################

import petl as etl
# activate bio extensions
import petlx.bio
table1 = (
    etl
    .fromvcf('fixture/sample.vcf', samples=None)
    .vcfunpackinfo()
)
table1


# vcfmeltsamples()
##################

import petl as etl
# activate bio extensions
import petlx.bio
table1 = (
    etl
    .fromvcf('fixture/sample.vcf')
    .vcfmeltsamples()
)
table1


# vcfunpackcall()
#################

import petl as etl
# activate bio extensions
import petlx.bio
table1 = (
    etl
    .fromvcf('fixture/sample.vcf')
    .vcfmeltsamples()
    .vcfunpackcall()
)
table1

