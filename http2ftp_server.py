# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
"""
Http Server support download ftp file

Authors: zhaoguowei(zhaoguowei@baidu.com)
Date:    2016-01-11 19:09
File:    http2ftp_server.py
"""
import tornado.ioloop
import tornado.web
import http2ftp
import logging
from tornado.options import define, options, parse_command_line

define("port", default=8080, help="The Http Server Port", type=int)
define("trunk_size", default=102400, help="The Download Chunk Size", type=int)
define("debug", default=True, help="Run Server In Debug Mode")


class FtpDownloadHandler(tornado.web.RequestHandler):
    def get(self):
        user_name = self.get_argument('user_name')
        passwd = self.get_argument('passwd')

        uri = self.request.path
        ftp_info = uri.split('/')
        host = ftp_info[1]
        file_path = '/'.join(ftp_info[2:])
        self.set_header("Content-Type", 'application/octet-stream')
        self.set_header("Content-Disposition", 'attachment; filename=%s' % ftp_info[-1])
        for chunk in http2ftp.get_file_trunks(host, file_path, user_name, passwd,
                                              options.trunk_size):
            self.write(chunk)
            self.flush()


def __main__():
    parse_command_line()
    app = tornado.web.Application([
        (r"^/.+$", FtpDownloadHandler),
    ], debug=options.debug)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    pass


if __name__ == '__main__':
    __main__()
