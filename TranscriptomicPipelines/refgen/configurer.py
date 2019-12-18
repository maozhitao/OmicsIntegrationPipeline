"""Preprocessing object for reference genome pipeline"""

import os

from const import ConfigurerConst
from utils.ftp import download

class Configurer(object):

    def __init__(self):
        self.config()

    def download_summary(self):
        download(
            ConfigurerConst.FTP_HOST,
            ConfigurerConst.FTP_PATH_SUMMARY,
            self.path_summary,
            't')

    def config(self):
        self.path_dir       = os.path.dirname(os.path.abspath(__file__))
        self.path_data      = ConfigurerConst.SEP_PATH.join([
            self.path_dir,
            ConfigurerConst.DATA_DIR])
        self.path_gff       = ConfigurerConst.SEP_PATH.join([
            self.path_data,
            ConfigurerConst.DATA_GFF])
        self.path_summary   = ConfigurerConst.SEP_PATH.join([
            self.path_data,
            ConfigurerConst.DATA_SUMMARY])

        self.download_summary()