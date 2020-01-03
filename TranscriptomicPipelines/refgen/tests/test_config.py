import os
import sys
sys.path.append('/'.join([os.path.abspath(os.path.dirname(__file__)), '..']))

from const import ConfigurerConst
from utils.ftp import download
from configurer import Configurer

def test():

    cfg = Configurer()
    cfg.config()

if __name__ == '__main__':

    test()