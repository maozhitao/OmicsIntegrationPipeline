from ftplib import FTP
import gzip
import zlib
import sys

class FtpConst(object):

    MODE_BIN        = 'b'
    MODE_TEXT       = 't'

    COMM_RETRIEVE   = 'RETR'
    COMM_STORE      = 'STOR'

    FORMAT          = 'utf-8'

    NEW_LINE        = '\n'
    SPACE           = ' '
    EMPTY           = ''
    EMPTY_BIN       = b''

    D_LOCAL         = 'output'

def download(host, filename, local, mode):
    """download a file on ftp server to the local

    input
        host        : (str) server host
        filename    : (str) path of target file on server
        path_local  : (str) path target file downloaded locally
        mode        : (str) 'b' for binary, 't' for text

    output
        None"""

    # FTP configuration
    ftp = FTP(host)
    ftp.encoding = FtpConst.FORMAT
    ftp.login()

    # Start reading from FTP server
    content_list = []

    if mode == FtpConst.MODE_TEXT:

        # text mode
        ftp.retrlines(
            cmd         = FtpConst.SPACE.join([FtpConst.COMM_RETRIEVE, filename]),
            callback    = content_list.append)
        content = FtpConst.NEW_LINE.join(content_list)
    
    elif mode == FtpConst.MODE_BIN:

        # binar mode
        ftp.retrbinary(
            cmd         = FtpConst.SPACE.join([FtpConst.COMM_RETRIEVE, filename]),
            callback    = content_list.append)
        if sys.version_info < (3, 0):
            import shutil
            with open('tmp.gzip','wb') as f:
                f.write((FtpConst.EMPTY_BIN.join(content_list)))
            with gzip.open('tmp.gzip','rb') as f_in, open(local, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                #content = f.read().decode(FtpConst.FORMAT)
        else:
            content = gzip.decompress(FtpConst.EMPTY_BIN.join(content_list)).decode(FtpConst.FORMAT)
            with open(local, 'wb') as f:
                f.write(bytes(content,'utf8'))
        
    else:
        raise ValueError("mode has to be either 't' (text) or 'b' (binary)")
    
    ftp.quit()

    '''
    # Write to local
    with open(local, 'wb') as f:
        if sys.version_info < (3, 0):
            f.write(bytes(content))
        else:
            f.write(bytes(content,'utf8'))
    '''