import os

class ConfigurerConst(object):

    FTP_HOST            = 'ftp.ncbi.nlm.nih.gov'
    FTP_PATH_SUMMARY    = 'genomes/refseq/assembly_summary_refseq.txt'

    DATA_DIR            = 'data'
    DATA_GFF            = 'gff'
    DATA_SUMMARY        = 'summary'

    SEP_PATH            = '/'

class ExtractorConst(object):

    FTP_HOST            = 'ftp.ncbi.nlm.nih.gov'
    FTP_URL_PREFIX_LEN  = 27

    FILE_EXT_TYPE       = 'genomic'
    FILE_EXT_FORMAT     = 'gff'
    FILE_EXT_SUFFIX     = 'gz'

    SEP_PART            = '_'
    SEP_FILE            = '.'
    SEP_PATH            = '/'