import pandas as pd
import os, sys


if (sys.version_info < (3, 0)):
    import const
    import utils.ftp as ftp
    import configurer
else:
    from . import const
    from . import configurer
    sys.path.insert(0,os.path.dirname(__file__))
    import utils.ftp as ftp


class RefGenRetriever(object):

    def __init__(self):
        self.cfg        = configurer.Configurer()

    def _load_summary(self):
        self.summary = pd.read_csv(
            self.cfg.path_summary,
            header  = 1,
            sep     = '\t',
            usecols = [0, 4, 7, 11, 12, 13, 17, 19],
            names   = ["asm_acc", "refseq_cat", "name", "level", "release",
                "genome", "gbrs", "ftp"])

    def _find_best_refseq(self, term):
        """look for the best refence genome candidate"""

        self.candid = None

        df = self.summary
        
        # 1. remove rows with gbrs, ftp columns of n.a.
        df = df[df.ftp != "na"]
        df = df[df.gbrs != "na"]
        
        # 2. choose rows related to the term
        df = df[df.name.str.contains(term) |
            df.name.str.contains(term.capitalize())]
        if df.shape[0] == 0:
            print("There is no available information for " + term)
            print("Please check your spelling.")
            return

        # 3. prioritize refseq_cat: representative -> reference -> na
        df_ = df[df.refseq_cat == "representative genome"]
        if df_.shape[0] == 0:
            df_ = df[df.refseq_cat == "reference genome"]
            if df_.shape[0] == 0:
                df_ = df[df.refseq_cat == "na"]
        df = df_
        
        # 4. prioritize level: complete -> chromesome -> scaffold >- config
        df_ = df[df.level == "Complete Genome"]
        if df_.shape[0] == 0:
            df_ = df[df.level == "Chromosome"]
            if df_.shape[0] == 0:
                df_ = df[df.level == "Scaffold"]
                if df_.shape[0] == 0:
                    df_ = df[df.level == "Contig"]
        df = df_
        
        # 5. prioritize release: major -> minor
        df_ = df[df.release == "Major"]
        if df_.shape[0] == 0:
            df_ = df[df.release == "Minor"]
            if df_.shape[0] == 0:
                df_ = df[df.release == "Patch"]
        df = df_
        
        # 6. prioritize genome: full -> partial
        df_ = df[df.genome == "Full"]
        if df_.shape[0] == 0:
            df_ = df[df.genome == "Partial"]
        
        self.candid = df_

    def download_refseq(self, term):
        self._load_summary()
        self._find_best_refseq(term)

        if self.candid is None:
            print("Quitting the process...")
            return
        
        # pick the first candid and parse the ftp path
        ftp_url         = self.candid.iloc[0].ftp
        ftp_dir_path    = ftp_url[const.ExtractorConst.FTP_URL_PREFIX_LEN:]
        file_prefix     = ftp_dir_path.split(const.ExtractorConst.SEP_PATH)[-1]
        
        file_ext        = const.ExtractorConst.SEP_FILE.join([
            const.ExtractorConst.FILE_EXT_TYPE,
            const.ExtractorConst.FILE_EXT_FORMAT,
            const.ExtractorConst.FILE_EXT_SUFFIX])
        
        file_gff_name   = const.ExtractorConst.SEP_PART.join([
            file_prefix,
            file_ext])
        
        file_path       = const.ExtractorConst.SEP_PATH.join([
            ftp_dir_path,
            file_gff_name])
        
        file_local      = const.ExtractorConst.SEP_PATH.join([
            self.cfg.path_gff,
            file_prefix,
            ])
            
        ftp.download(
            const.ExtractorConst.FTP_HOST,
            file_path,
            file_local,
            'b')
            
        return file_local

if __name__ == '__main__':

    term = 'Escherichia coli'
    r_refgen = RefGenRetriever()
    file_local = r_refgen.download_refseq(term)