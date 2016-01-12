# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
"""
Trans http request to ftp

Authors: zhaoguowei(zhaoguowei@baidu.com)
Date:    2016-01-11 17:56
File:    http2ftp.py
"""
import ftplib
import ftputil.session
import ftputil
import logging

my_session_factory = ftputil.session.session_factory(
        base_class=ftplib.FTP_TLS,
        port=31,
        encrypt_data_channel=True,
        debug_level=2)


def get_file_trunks(host, file_path, user_name, passwd, chunk_size=1024):
    logging.debug("Begin Download Ftp File %s in %s with %s@%s (size=%s)" % (
        file_path, host, user_name, passwd, chunk_size))
    with ftputil.FTPHost(host, user_name, passwd) as ftp_host:
        try:
            file_obj = None
            file_obj = ftp_host.open(file_path, 'rb')
            while True:
                chunk = file_obj.read(chunk_size)
                if not chunk:
                    break
                yield chunk
        except IOError as err:
            raise err
        finally:
            if file_obj is not None:
                file_obj.close()
        pass


def list_dir(host, file_path, user_name, passwd):
    with ftputil.FTPHost(host, user_name, passwd) as ftp_host:
        try:
            return ftp_host.listdir(file_path)
        except IOError as err:
            raise err
        finally:
            pass
        pass
    pass


def __main__():
    fp = open('test.ipa', 'w+')
    for trunk in get_file_trunks('127.0.0.1',
                                 '/data/output/test.ipa',
                                 'ftp', 'ftp'):
        fp.write(trunk)
        print 'Download File Trunk'
    fp.close()
    pass


if __name__ == '__main__':
    __main__()
