from petlx.tabix import fromtabix
from petl.testutils import ieq


def test_fromtabix():
    actual = fromtabix('fixture/test.bed.gz', region='Pf3D7_02_v3:110000-120000')
    expect = (('#chrom', 'start', 'end', 'region'),
              ('Pf3D7_02_v3', '105800', '447300', 'Core'))
    ieq(expect, actual)
    
    
def test_fromtabix_noheader():
    actual = fromtabix('fixture/test_noheader.bed.gz', region='Pf3D7_02_v3:110000-120000')
    expect = (('Pf3D7_02_v3', '105800', '447300', 'Core'),)
    ieq(expect, actual)
    