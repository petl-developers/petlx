# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division


import petl as etl
from petl.test.helpers import ieq


# activate extension
import petlx.bio.tabix


def test_fromtabix():
    actual = etl.fromtabix('fixture/test.bed.gz',
                           region='Pf3D7_02_v3:110000-120000')
    expect = (('#chrom', 'start', 'end', 'region'),
              ('Pf3D7_02_v3', '105800', '447300', 'Core'))
    ieq(expect, actual)
    
    
def test_fromtabix_noheader():
    actual = etl.fromtabix('fixture/test_noheader.bed.gz',
                           region='Pf3D7_02_v3:110000-120000')
    expect = (('Pf3D7_02_v3', '105800', '447300', 'Core'),)
    ieq(expect, actual)
