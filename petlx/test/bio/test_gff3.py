# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division


import petl as etl
from petl.test.helpers import eq_


# activate extension
import petlx.bio.gff3
from petlx.bio.gff3 import GFF3_HEADER


sample_gff3_filename = 'fixture/sample.gff'


def test_fromgff3():
    
    features = etl.fromgff3(sample_gff3_filename)
    
    eq_(GFF3_HEADER, features.header())

    row = list(features)[1]
    eq_('apidb|MAL1', row[0])
    eq_('ApiDB', row[1])
    eq_('supercontig', row[2])
    eq_(1, row[3])
    eq_(643292, row[4])
    eq_('.', row[5])
    eq_('+', row[6])
    eq_('.', row[7])
    eq_('apidb|MAL1', row[8]['ID']) 
    eq_('MAL1', row[8]['Name'])
    eq_('Plasmodium falciparum', row[8]['organism_name'])
    

def test_fromgff3_trailing_semicolon():
    
    features = etl.fromgff3(sample_gff3_filename)
    
    row = list(features)[2]
    eq_('apidb|MAL2', row[0])
    eq_('ApiDB', row[1])
    eq_('supercontig', row[2])
    eq_(1, row[3])
    eq_(947102, row[4])
    eq_('.', row[5])
    eq_('+', row[6])
    eq_('.', row[7])
    eq_('apidb|MAL2', row[8]['ID']) 
    eq_('MAL2', row[8]['Name'])
    eq_('Plasmodium falciparum', row[8]['organism_name'])


def test_fromgff3_region():
    tbl_features = etl.fromgff3('fixture/sample.sorted.gff.gz',
                                region='apidb|MAL5')
    eq_(7, tbl_features.nrows())
    tbl_features = etl.fromgff3('fixture/sample.sorted.gff.gz',
                                region='apidb|MAL5:1289593-1289595')
    eq_(4, tbl_features.nrows())
