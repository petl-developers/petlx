"""
Tests for the gff3 module.

"""
from tempfile import NamedTemporaryFile
from nose.tools import eq_
from petl.util import header, nrows

from petlx.gff3 import fromgff3, gff3lookup, gff3join, gff3_parse_attributes,\
    gff3leftjoin
from petl.transform import selecteq
from petl.testutils import ieq
import petl.fluent as etl


sample_gff3_filename = 'fixture/sample.gff'


def test_fromgff3():
    
    features = fromgff3(sample_gff3_filename)
    
    expect_header = ('seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes')
    eq_(expect_header, header(features))

    # apidb|MAL1    ApiDB    supercontig    1    643292    .    +    .    ID=apidb|MAL1;Name=MAL1;description=MAL1;size=643292;web_id=MAL1;molecule_type=dsDNA;organism_name=Plasmodium falciparum;translation_table=11;topology=linear;localization=nuclear;Dbxref=ApiDB_PlasmoDB:MAL1,GenBank:NC_004325,taxon:36329
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
    
    # test data wrapped in hybrid rows
    eq_('apidb|MAL1', row['seqid'])
    eq_('ApiDB', row['source'])
    eq_('supercontig', row['type'])
    eq_(1, row['start'])
    eq_(643292, row['end'])
    eq_('.', row['score'])
    eq_('+', row['strand'])
    eq_('.', row['phase'])
    eq_('apidb|MAL1', row['attributes']['ID']) 
    eq_('MAL1', row['attributes']['Name'])
    eq_('Plasmodium falciparum', row['attributes']['organism_name'])
    
    
def test_fromgff3_trailing_semicolon():
    
    features = fromgff3(sample_gff3_filename)
    
    #apidb|MAL2    ApiDB    supercontig    1    947102    .    +    .    ID=apidb|MAL2;Name=MAL2;description=MAL2;size=947102;web_id=MAL2;molecule_type=dsDNA;organism_name=Plasmodium falciparum;translation_table=11;topology=linear;localization=nuclear;Dbxref=ApiDB_PlasmoDB:MAL2,GenBank:NC_000910,taxon:36329;
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
    
    
def test_gff3lookup():
    
    features = fromgff3(sample_gff3_filename)
    genes = selecteq(features, 'type', 'gene')
    lkp = gff3lookup(genes)
    
    #apidb|MAL1    ApiDB    gene    56913    57116    .    -    .    ID=apidb|PFA0035c;Name=PFA0035c;description=hypothetical+protein%2C+conserved+in+P.+falciparum;size=204;web_id=PFA0035c;locus_tag=PFA0035c;size=204;Alias=MAL1P4.06b

    actual = lkp['apidb|MAL1'][56911:56915]
    eq_(1, len(actual))
    eq_(56913, actual[0][3])
    eq_(57116, actual[0][4])

    actual = lkp['apidb|MAL1'][56915]
    eq_(1, len(actual))
    eq_(56913, actual[0][3])
    eq_(57116, actual[0][4])


def test_gff3join():    

    #apidb|MAL1    ApiDB    gene    56913    57116    .    -    .    ID=apidb|PFA0035c;Name=PFA0035c;description=hypothetical+protein%2C+conserved+in+P.+falciparum;size=204;web_id=PFA0035c;locus_tag=PFA0035c;size=204;Alias=MAL1P4.06b
    snps = (('chr', 'pos'),
            ('apidb|MAL1', 56911),
            ('apidb|MAL1', 56915))
    features = fromgff3(sample_gff3_filename)
    genes = selecteq(features, 'type', 'gene')
    actual = gff3join(snps, genes, seqid='chr', start='pos', end='pos')
    expect = (('chr', 'pos', 'seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes'),
              ('apidb|MAL1', 56915, 'apidb|MAL1', 'ApiDB', 'gene', 56913, 57116, '.', '-', '.', gff3_parse_attributes("ID=apidb|PFA0035c;Name=PFA0035c;description=hypothetical+protein%2C+conserved+in+P.+falciparum;size=204;web_id=PFA0035c;locus_tag=PFA0035c;size=204;Alias=MAL1P4.06b")))
    ieq(expect, actual)
    ieq(expect, actual)
    
    
def test_gff3leftjoin():    

    #apidb|MAL1    ApiDB    gene    56913    57116    .    -    .    ID=apidb|PFA0035c;Name=PFA0035c;description=hypothetical+protein%2C+conserved+in+P.+falciparum;size=204;web_id=PFA0035c;locus_tag=PFA0035c;size=204;Alias=MAL1P4.06b
    snps = (('chr', 'pos'),
            ('apidb|MAL1', 56911),
            ('apidb|MAL1', 56915))
    features = fromgff3(sample_gff3_filename)
    genes = selecteq(features, 'type', 'gene')
    actual = gff3leftjoin(snps, genes, seqid='chr', start='pos', end='pos')
    expect = (('chr', 'pos', 'seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes'),
              ('apidb|MAL1', 56911, None, None, None, None, None, None, None, None, None),
              ('apidb|MAL1', 56915, 'apidb|MAL1', 'ApiDB', 'gene', 56913, 57116, '.', '-', '.', gff3_parse_attributes("ID=apidb|PFA0035c;Name=PFA0035c;description=hypothetical+protein%2C+conserved+in+P.+falciparum;size=204;web_id=PFA0035c;locus_tag=PFA0035c;size=204;Alias=MAL1P4.06b")))
    ieq(expect, actual)
    ieq(expect, actual)
    
    
def test_integration():
    #apidb|MAL1    ApiDB    gene    56913    57116    .    -    .    ID=apidb|PFA0035c;Name=PFA0035c;description=hypothetical+protein%2C+conserved+in+P.+falciparum;size=204;web_id=PFA0035c;locus_tag=PFA0035c;size=204;Alias=MAL1P4.06b
    snps = etl.wrap((('chr', 'pos'),
                     ('apidb|MAL1', 56911),
                     ('apidb|MAL1', 56915)))
    features = etl.fromgff3(sample_gff3_filename)
    genes = features.selecteq('type', 'gene')
    actual = snps.gff3join(genes, seqid='chr', start='pos', end='pos')
    expect = (('chr', 'pos', 'seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes'),
              ('apidb|MAL1', 56915, 'apidb|MAL1', 'ApiDB', 'gene', 56913, 57116, '.', '-', '.', gff3_parse_attributes("ID=apidb|PFA0035c;Name=PFA0035c;description=hypothetical+protein%2C+conserved+in+P.+falciparum;size=204;web_id=PFA0035c;locus_tag=PFA0035c;size=204;Alias=MAL1P4.06b")))
    ieq(expect, actual)
    ieq(expect, actual)
    

def test_fromgff3_region():
    tbl_features = fromgff3('fixture/sample.sorted.gff.gz', region='apidb|MAL5')
    eq_(7, nrows(tbl_features))
    tbl_features = fromgff3('fixture/sample.sorted.gff.gz', region='apidb|MAL5:1289593-1289595')
    eq_(4, nrows(tbl_features))
