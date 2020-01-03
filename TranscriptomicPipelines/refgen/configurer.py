"""Preprocessing object for reference genome pipeline"""

import os
import sys
if (sys.version_info < (3, 0)):
    import const
    import utils.ftp as ftp
else:
    from . import const
    from . import configurer
    sys.path.insert(0,os.path.dirname(__file__))
    import utils.ftp as ftp

class Configurer(object):

    def __init__(self):
        self.config()

    def download_summary(self):
        ftp.download(
            const.ConfigurerConst.FTP_HOST,
            const.ConfigurerConst.FTP_PATH_SUMMARY,
            self.path_summary,
            't')

    def config(self):
        self.path_dir       = os.path.dirname(os.path.abspath(__file__))
        self.path_data      = const.ConfigurerConst.SEP_PATH.join([
            self.path_dir,
            const.ConfigurerConst.DATA_DIR])
        self.path_gff       = const.ConfigurerConst.SEP_PATH.join([
            self.path_data,
            const.ConfigurerConst.DATA_GFF])
        self.path_summary   = const.ConfigurerConst.SEP_PATH.join([
            self.path_data,
            const.ConfigurerConst.DATA_SUMMARY])

        self.download_summary()