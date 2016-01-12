# Simple tool to proxy ftp download request use http server
## Why
One of our company service only provide ftp server to download packages, but we need a http server to download file to install in iPhone
So I use tornado and ftputil to build this small tool to support this.

## What need
ftputil: `pip install ftputil`

tornado: `pip install tornado`

## How to use
1. start the http2ftp_server

2. Send http://host:port/ftphost/ftp_file_path?user_name=xxxx&passwd=xxxxx